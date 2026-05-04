# api/views.py
from django.conf import settings
from rest_framework import status, generics
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CustomUserSerializer,
    SetNewPasswordSerializer,
    ResetPasswordEmailRequestSerializer,
    UserRegistrationSerializer,
    ProductImageExtractionSerializer, PurchaseIntentionSerializer, ReflectionQuestionSerializer,
    FinalDecisionUpdateSerializer, AppFeedbackSerializer, AdminFeedbackSerializer
)
from .models import CustomUser, ErrorLog, PurchaseIntention, ReflectionQuestion, SavingsGoal, AppFeedback
from .services import verify_google_token, send_password_reset_email, generate_ai_verdict, extract_product_data_via_ai, \
    generate_reflection_questions, generate_gemini_json_response, log_app_error
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
import json
from google import genai
from google.genai import types
from django.utils.translation import gettext_lazy as _


def get_user_tokens(user):
    """Helper to generate JWTs for the Vue.js frontend."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(auth_provider='email')
            tokens = get_user_tokens(user)
            return Response({
                'message': _('Inscription réussie.'),
                'tokens': tokens,
                'user': {'email': user.email, 'budget': user.monthly_budget}
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # 1. Vérification préventive du fournisseur (Auth Provider)
        try:
            user_check = CustomUser.objects.get(email=email)
            if user_check.auth_provider == 'google':
                return Response(
                    {'error': _(
                        "Cette adresse e-mail est liée à Google. Veuillez utiliser le bouton 'Se connecter avec Google'.")},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except CustomUser.DoesNotExist:
            # L'utilisateur n'existe pas du tout, on laisse la suite gérer
            pass

        # 2. Authentification classique
        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = get_user_tokens(user)
            return Response({
                'message': _('Connexion réussie.'),
                'tokens': tokens
            }, status=status.HTTP_200_OK)

        return Response({'error': _('E-mail ou mot de passe incorrect.')}, status=status.HTTP_401_UNAUTHORIZED)


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('credential')
        user_data = verify_google_token(token)

        if not user_data:
            return Response({'error': _('Échec de l’authentification Google. Vérifiez votre compte et réessayez')}, status=status.HTTP_400_BAD_REQUEST)

        email = user_data.get('email')

        # 1. Vérification du compte existant
        try:
            user = CustomUser.objects.get(email=email)
            if user.auth_provider != CustomUser.AuthProviders.GOOGLE:
                # Le message précis qui sera affiché sur le front-end
                return Response(
                    {'error': _(
                        "Ce compte utilise un mot de passe. Veuillez utiliser le formulaire de connexion classique en haut.")},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            # 2. Création du compte Google s'il n'existe pas
            user = CustomUser.objects.create_user(
                email=email,
                password=None,
                auth_provider=CustomUser.AuthProviders.GOOGLE,
            )

        tokens = get_user_tokens(user)
        return Response({
            'message': _('Authentification Google réussie.'),
            'tokens': tokens
        }, status=status.HTTP_200_OK)


class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordEmailRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)

                # Bloquer silencieusement si l'utilisateur s'est inscrit via Google
                if user.auth_provider == 'GOOGLE':
                    return Response(
                        {'error': _("Ce compte est lié à Google. Veuillez utiliser la connexion Google.")},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 1. Générer l'identifiant encodé et le token de sécurité
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = PasswordResetTokenGenerator().make_token(user)

                # 2. Construire le lien qui pointera vers le front-end VUE.JS
                # (Ex: http://localhost:5173/reset-password/MTE/ajk123-token...)
                frontend_url = settings.FRONTEND_URL
                reset_url = f"{frontend_url}/reset-password/{uidb64}/{token}/"

                # 3. Envoyer l'e-mail via le service
                send_password_reset_email(email, reset_url)

            except CustomUser.DoesNotExist:
                # RÈGLE DE SÉCURITÉ : Ne jamais confirmer à un attaquant si un e-mail existe en base
                pass

            # On renvoie un message de succès générique dans tous les cas
            return Response(
                {'message': _(
                    "Si votre adresse e-mail existe dans notre base de données, vous recevrez un lien de réinitialisation sous peu.")},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        serializer = SetNewPasswordSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Decode the user ID
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = CustomUser.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                user = None

            # Verify the token is valid for this specific user
            if user is not None and PasswordResetTokenGenerator().check_token(user, token):
                # Set the new password securely
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response(
                    {'message': _('Votre mot de passe a été réinitialisé avec succès.')},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': _('Le lien de réinitialisation est invalide ou a expiré.')},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    # This ensures only requests with a valid JWT can access this view
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        # On utilise 'partial=True' pour permettre de ne modifier que certains champs
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": _("Votre profil a été mis à jour avec succès."),
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExtractProductInfoView(APIView):
    """
    Reçoit l'image depuis Vue.js, interroge l'IA et renvoie les données extraites
    pour la phase de 'Vérification' (sans sauvegarder l'intention d'achat).
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = ProductImageExtractionSerializer(data=request.data)

        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            try:
                extracted_data = extract_product_data_via_ai(image_file)
                return Response({
                    "message": _("Extraction réussie. Veuillez vérifier les informations."),
                    "data": extracted_data
                }, status=status.HTTP_200_OK)

            except Exception as e:
                # Journalisation de l'erreur d'API IA dans la base de données
                log_app_error(e, endpoint_url=request.path, user=request.user)
                return Response(
                    {"error": _(
                        "Impossible d'analyser l'image. L'IA est momentanément indisponible. Veuillez saisir les informations manuellement.")},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseIntentionCreateView(APIView):
    """
    Crée l'intention d'achat finale une fois que l'utilisateur a validé
    (soit après extraction corrigée, soit après saisie 100% manuelle).
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = PurchaseIntentionSerializer(data=request.data)

        if serializer.is_valid():
            # Vérifie si l'utilisateur a forcé le passage
            is_bypassed = serializer.validated_data.get('is_incoherent_bypassed', False)

            # Si non forcé, on fait l'analyse de cohérence via l'IA
            if not is_bypassed:
                product_name = serializer.validated_data.get('product_name', '')
                product_category = serializer.validated_data.get('product_category', '')
                product_price = serializer.validated_data.get('product_price', 0)
                preferred_currency = getattr(request.user, 'preferred_currency', 'TND')

                prompt = f"""
                Vérifie la cohérence de cette intention d'achat :
                Nom : "{product_name}"
                Catégorie : "{product_category}"
                Prix : {product_price} {preferred_currency}

                Est-ce que ces trois éléments sont logiquement cohérents ensemble dans la réalité ? 
                Réponds STRICTEMENT par un JSON : {{"is_coherent": true/false, "reason": "explication brève"}}
                """
                try:

                    result = generate_gemini_json_response(prompt)

                    # On bloque si l'IA trouve ça incohérent
                    if not result.get('is_coherent', True):
                        return Response({
                            "error": result.get('reason',
                                                'Ces informations semblent incohérentes. Veuillez les vérifier.')
                        }, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    # En cas d'erreur IA, on log et on laisse passer
                    log_app_error(e, context_message="Échec du garde-frontière IA", endpoint_url=request.path,
                                  user=request.user, level=ErrorLog.LogLevels.WARNING)

            # Sauvegarde finale
            purchase_intention = serializer.save(user=request.user)

            return Response({
                "message": _("Les informations ont été validées. L'IA prépare ses questions."),
                "id": purchase_intention.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateQuestionsView(APIView):
    """
    Déclenche la génération des 3 questions par l'IA pour une intention donnée.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, intention_id):
        try:
            intention = get_user_intention_or_404(intention_id, request.user)
            if intention.questions.exists():
                questions = intention.questions.all()
            else:
                questions = generate_reflection_questions(intention.id)
            serializer = ReflectionQuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound as e:
            # Let DRF handle the 404 naturally or catch it if you prefer custom formatting
            return Response({"error": str(e.detail)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": _("L'IA n'a pas pu générer les questions. Veuillez réessayer.")},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerateVerdictView(APIView):
    """
    Récupère les réponses aux questions, déclenche l'IA pour le verdict et met à jour l'intention.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, intention_id):
        try:
            with transaction.atomic():
                # 1. Vérification de sécurité : l'intention doit appartenir à l'utilisateur
                intention = get_user_intention_or_404(intention_id, request.user)

                # 2. Sauvegarde des réponses envoyées par Vue.js
                # On s'attend à recevoir : {"answers": [{"id": 1, "answer": "YES"}, ...]}
                answers_data = request.data.get('answers', [])
                for item in answers_data:
                    question = ReflectionQuestion.objects.filter(id=item.get('id'),
                                                                 purchase_intention=intention).first()
                    if question and item.get('answer'):
                        question.user_answer = str(item.get('answer'))
                        question.save()

                # 3. On vérifie que toutes les questions ont une réponse
                unanswered_count = intention.questions.filter(user_answer__isnull=True).count()
                if unanswered_count > 0:
                    return Response(
                        {"error": _("Veuillez répondre à toutes les questions avant d'obtenir le verdict.")},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 4. Génération du verdict via l'IA
                updated_intention = generate_ai_verdict(intention.id)

                # 5. Retour des données au front
                serializer = PurchaseIntentionSerializer(updated_intention)
            return Response(serializer.data, status=status.HTTP_200_OK)


        except NotFound as e:

            return Response({"error": str(e.detail)}, status=status.HTTP_404_NOT_FOUND)

        except Exception:

            return Response({"error": _("L'IA n'a pas pu rendre son verdict. Veuillez réessayer.")},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserFinalDecisionView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, intention_id):
        try:
            intention = get_user_intention_or_404(intention_id, request.user)
            serializer = FinalDecisionUpdateSerializer(intention, data=request.data, partial=True)

            if serializer.is_valid():
                updated_intention = serializer.save()

                # Gestion du chronomètre si la décision est "CALM" (Attendre)
                if updated_intention.user_final_decision == PurchaseIntention.DecisionChoices.CALM_DOWN:
                    hours = request.user.cooldown_preference or 24
                    updated_intention.cooldown_expires_at = timezone.now() + timedelta(hours=hours)
                else:
                    # On nettoie si l'utilisateur achète ou abandonne
                    updated_intention.cooldown_expires_at = None

                updated_intention.save(update_fields=['cooldown_expires_at'])

                return Response({
                    "message": _("Votre décision finale a été enregistrée. Merci pour votre honnêteté !"),
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({"error": str(e.detail)}, status=status.HTTP_404_NOT_FOUND)


class DashboardSummaryView(APIView):
    """
    Vue unique et centralisée pour le Tableau de Bord.
    Renvoie les stats, le ratio, les objectifs, l'historique et les rappels.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now()
        # Remise à UNKOWN des délais expirés
        PurchaseIntention.objects.filter(
            user=user,
            user_final_decision=PurchaseIntention.DecisionChoices.CALM_DOWN,
            cooldown_expires_at__lte=now
        ).update(
            user_final_decision=PurchaseIntention.DecisionChoices.UNKOWN,
            cooldown_expires_at=None
        )

        # 1. Économies du mois
        monthly_savings = PurchaseIntention.objects.filter(
            user=user,
            user_final_decision=PurchaseIntention.DecisionChoices.ABANDON,
            created_at__year=now.year,
            created_at__month=now.month
        ).aggregate(total=Sum('product_price'))['total'] or 0.00

        # 2. Ratio de Maîtrise (Basé uniquement sur les décisions finalisées)
        # On exclut les intentions 'UNKOWN' ou nulles pour ne pas fausser le ratio
        resolved_intentions = PurchaseIntention.objects.filter(
            user=user,
            created_at__year=now.year,
            created_at__month=now.month
        ).exclude(
            Q(user_final_decision__isnull=True) | Q(user_final_decision=PurchaseIntention.DecisionChoices.UNKOWN)
        )

        total_resolved = resolved_intentions.count()
        abandoned_intentions = resolved_intentions.filter(
            user_final_decision=PurchaseIntention.DecisionChoices.ABANDON
        ).count()

        mastery_ratio = int((abandoned_intentions / total_resolved) * 100) if total_resolved > 0 else 0

        # 3. Objectif d'épargne actif
        active_goal = SavingsGoal.objects.filter(user=user, is_active=True).first()
        goal_data = {
            "goal_name": active_goal.goal_name,
            "target_amount": float(active_goal.target_amount),
            "saved_amount": float(active_goal.saved_amount)
        } if active_goal else None

        # 4. Historique récent (5 derniers éléments)
        recent_intentions = PurchaseIntention.objects.filter(user=user).order_by('-created_at')[:5]
        history_serializer = PurchaseIntentionSerializer(recent_intentions, many=True)

        # 5. Analyses en attente (Bannière de rappel)
        pending_intentions = PurchaseIntention.objects.filter(
            user=user
        ).filter(
            Q(user_final_decision__isnull=True) | Q(user_final_decision=PurchaseIntention.DecisionChoices.UNKOWN)
        ).order_by('-created_at')
        pending_serializer = PurchaseIntentionSerializer(pending_intentions, many=True)

        # Construction de la réponse unifiée
        return Response({
            "user_name": user.first_name or "Utilisateur",
            "ai_coach_message": "Vous avez fait de superbes économies ce mois-ci !" if monthly_savings > 0 else "Prêt à sauver votre budget ?",
            "mastery_ratio": mastery_ratio,
            "savings_goal": goal_data,
            "stats": {
                "monthly_savings": float(monthly_savings),
                "current_month": now.strftime('%B'),
            },
            "recent_history": history_serializer.data,
            "pending_intentions": pending_serializer.data
        }, status=status.HTTP_200_OK)


class AppFeedbackCreateView(APIView):
    """
    Reçoit l'objet, le message (comment) et la note.
    Enregistre uniquement en base de données pour consultation par l'admin.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AppFeedbackSerializer(data=request.data)

        if serializer.is_valid():
            # Enregistre le feedback et l'associe à l'utilisateur connecté
            serializer.save(user=request.user)

            return Response({
                "message": "Votre message a été envoyé avec succès !"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatsDashboardAPIView(APIView):
    def get(self, request):
        user = request.user
        period = request.query_params.get('period', 'month')
        category = request.query_params.get('category')

        # 1. Définition de la plage temporelle dynamique
        now = timezone.now()
        query_filter = Q(user=user)

        if period == 'today':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            query_filter &= Q(created_at__gte=start_date)
        elif period == 'year':
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            query_filter &= Q(created_at__gte=start_date)
        elif period == 'month':
            # Optionnel: 30 derniers jours ou depuis le 1er du mois. Ici, 30 derniers jours.
            start_date = now - timedelta(days=30)
            query_filter &= Q(created_at__gte=start_date)
        # Si period == 'all', on n'ajoute pas de filtre de date

        # 2. Construction du filtre par catégorie
        if category:
            query_filter &= Q(product_category=category)

        # 3. Agrégations directes via PostgreSQL
        stats = PurchaseIntention.objects.filter(query_filter).aggregate(
            total_saved=Sum('product_price', filter=Q(user_final_decision=PurchaseIntention.DecisionChoices.ABANDON)),
            count_abandoned=Count('id', filter=Q(user_final_decision=PurchaseIntention.DecisionChoices.ABANDON)),
            count_bought=Count('id', filter=Q(user_final_decision=PurchaseIntention.DecisionChoices.BUY)),
            count_waiting=Count('id', filter=Q(user_final_decision=PurchaseIntention.DecisionChoices.CALM_DOWN)),
        )

        # Nettoyage des valeurs Null
        total_saved = stats['total_saved'] or 0.00
        count_abandoned = stats['count_abandoned'] or 0
        count_bought = stats['count_bought'] or 0
        count_waiting = stats['count_waiting'] or 0

        # 4. Calcul du ratio de maîtrise (uniquement sur les décisions finales résolues)
        total_resolved = count_abandoned + count_bought
        mastery_rate = (count_abandoned / total_resolved * 100) if total_resolved > 0 else 0

        return Response({
            "summary": {
                "total_saved": float(total_saved),
                "abandoned_count": count_abandoned,
                "mastery_rate": round(mastery_rate, 1)
            },
            "chart_data": [
                {"label": "Abandonnés", "value": count_abandoned, "color": "#5A877E"},
                {"label": "Achetés", "value": count_bought, "color": "#EF4444"},
                {"label": "En réflexion", "value": count_waiting, "color": "#F59E0B"},
            ]
        })


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class PurchaseHistoryView(generics.ListAPIView):
    """
    Endpoint intelligent pour la page de suivi.
    Sépare automatiquement les requêtes "En réflexion" des requêtes "Historique".
    """
    serializer_class = PurchaseIntentionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        queryset = PurchaseIntention.objects.filter(user=user)

        # 1. FILTRE INTELLIGENT DU STATUT (Gère la séparation Haut/Bas)
        status_param = self.request.query_params.get('status')

        if status_param == 'Attendre':
            # Requête venant de la liste "En période de réflexion" (Haut)
            queryset = queryset.filter(user_final_decision=PurchaseIntention.DecisionChoices.CALM_DOWN)

        elif status_param in ['Acheté', 'Achet ']:
            # Requête venant des filtres de l'historique (Bas) - Tolérance pour les accents
            queryset = queryset.filter(user_final_decision=PurchaseIntention.DecisionChoices.BUY)

        elif status_param in ['Abandonné', 'Abandonn ']:
            # Requête venant des filtres de l'historique (Bas) - Tolérance pour les accents
            queryset = queryset.filter(user_final_decision=PurchaseIntention.DecisionChoices.ABANDON)

        else:
            # Requête par défaut (status='all') pour l'historique (Bas)
            # On exclut "Attendre" et "Inconnu" pour n'afficher que les actions clôturées
            queryset = queryset.filter(user_final_decision__in=[
                PurchaseIntention.DecisionChoices.BUY,
                PurchaseIntention.DecisionChoices.ABANDON
            ])

        # 2. FILTRE CATÉGORIE
        category = self.request.query_params.get('category')
        if category and category != 'all':
            queryset = queryset.filter(product_category=category)

        # 3. FILTRE RECHERCHE
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(product_name__icontains=search)

        # 4. FILTRE PRIX
        price = self.request.query_params.get('price')
        if price and price != 'all':
            if price == 'under500':
                queryset = queryset.filter(product_price__lt=500)
            elif price == '500to1500':
                queryset = queryset.filter(product_price__gte=500, product_price__lte=1500)
            elif price == 'over1500':
                queryset = queryset.filter(product_price__gt=1500)

        # 5. TRI
        sort_by = self.request.query_params.get('sort_by', 'date')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('product_price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-product_price')
        elif sort_by == 'category':
            queryset = queryset.order_by('product_category')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset


class AdminFeedbackListView(APIView):
    """
    Endpoint exclusif pour les administrateurs pour lire les tickets de support.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]  # Bloque les utilisateurs normaux

    def get(self, request):
        # Fetch all feedbacks, newest first
        feedbacks = AppFeedback.objects.all().order_by('-created_at')
        serializer = AdminFeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PurchaseIntentionDetailView(generics.RetrieveAPIView):
    """
    Permet de récupérer les détails d'une intention d'achat spécifique (pour la reprise de l'analyse).
    """
    serializer_class = PurchaseIntentionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'intention_id'

    def get_queryset(self):
        # Sécurité : l'utilisateur ne peut récupérer que ses propres intentions
        return PurchaseIntention.objects.filter(user=self.request.user)


def get_user_intention_or_404(intention_id, user):
    """Fetches a PurchaseIntention or raises a DRF NotFound exception."""
    try:
        return PurchaseIntention.objects.get(id=intention_id, user=user)
    except PurchaseIntention.DoesNotExist:
        raise NotFound(detail=_("Intention d'achat introuvable."))
