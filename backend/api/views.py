# api/views.py
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CustomUserSerializer,
    SetNewPasswordSerializer,
    ResetPasswordEmailRequestSerializer,
    UserRegistrationSerializer
)
from .models import CustomUser
from .services import verify_google_token, send_password_reset_email


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
            return Response({'error': _('Jeton Google invalide.')}, status=status.HTTP_400_BAD_REQUEST)

        email = user_data.get('email')

        # 1. Vérification du compte existant
        try:
            user = CustomUser.objects.get(email=email)
            if user.auth_provider != 'google':
                # Le message précis qui sera affiché sur le front-end
                return Response(
                    {'error': _("Ce compte utilise un mot de passe. Veuillez utiliser le formulaire de connexion classique en haut.")},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            # 2. Création du compte Google s'il n'existe pas
            user = CustomUser.objects.create_user(
                email=email,
                password=None,
                auth_provider='google',
            )

        tokens = get_user_tokens(user)
        return Response({
            'message': _('Authentification Google réussie.'),
            'tokens': tokens
        }, status=status.HTTP_200_OK)


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