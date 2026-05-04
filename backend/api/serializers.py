from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, PurchaseIntention, ReflectionQuestion, AppFeedback, ErrorLog
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'monthly_budget', 'profession',
            'financial_goal', 'location_data', 'auth_provider', 'is_staff', 'cooldown_preference', 'evaluation_rigor','preferred_currency'
        ]
        extra_kwargs = {
            'email': {'read_only': True},
            'username': {'read_only': True},
            'is_staff': {'read_only': True}
        }

    def validate_monthly_budget(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(_("Le budget mensuel ne peut pas être négatif."))
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        error_messages={
            'blank': _('Le mot de passe est obligatoire.'),
            'required': _('Ce champ est requis.')
        }
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        error_messages={
            'blank': _('La confirmation du mot de passe est obligatoire.'),
            'required': _('Ce champ est requis.')
        }
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'confirm_password', 'monthly_budget', 'profession']
        extra_kwargs = {
            'email': {
                'required': True,
                'error_messages': {
                    'blank': _("L'adresse e-mail est obligatoire."),
                    'invalid': _("Veuillez entrer une adresse e-mail valide.")
                }
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        # API rejection if passwords do not match
        if password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": _("Les mots de passe ne correspondent pas.")
            })

        # Optional: You can also enforce Django's built-in validate_password(password) here
        # to mirror what you did in SetNewPasswordSerializer

        return attrs

    def create(self, validated_data):
        # Remove confirm_password because it doesn't exist on the CustomUser model
        validated_data.pop('confirm_password', None)

        # Hachage sécurisé du mot de passe avant l'enregistrement dans PostgreSQL
        validated_data['password'] = make_password(validated_data.get('password'))

        # Création de l'utilisateur avec les données validées et sécurisées
        return super().create(validated_data)
def validate_not_empty_string(value, error_message):
    """Utility to ensure string fields are not just whitespace."""
    if not value.strip():
        raise serializers.ValidationError(error_message)
    return value

class ReflectionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReflectionQuestion
        fields = ['id', 'purchase_intention', 'question_text','ai_options', 'user_answer']


class PurchaseIntentionSerializer(serializers.ModelSerializer):
    # Matches the related_name='questions' in the ReflectionQuestion model
    questions = ReflectionQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseIntention
        fields = [
            'id', 'user', 'product_name', 'product_price', 'product_category',
            'product_image', 'ai_verdict', 'ai_reasoning', 'user_final_decision',
            'created_at', 'updated_at', 'questions', 'usage_frequency', 'has_similar_item', 'urgency_level',
            'cooldown_expires_at','is_incoherent_bypassed'
        ]
        read_only_fields = [
            'id', 'user', 'ai_verdict', 'ai_reasoning',
            'user_final_decision', 'created_at', 'updated_at', 'cooldown_expires_at'
        ]

        def validate_product_price(self, value):
            """Valide que le prix est strictement positif."""
            if value <= 0:
                raise serializers.ValidationError(_("Le prix du produit doit être strictement positif."))
            return value

        def validate_product_name(self, value):
            """Évite qu'un utilisateur envoie un nom de produit composé uniquement d'espaces."""
            return validate_not_empty_string(value, _("Le nom du produit est obligatoire."))

        def validate_product_category(self, value):
            return validate_not_empty_string(value, _("La catégorie du produit est obligatoire."))


class ErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = '__all__'
        # Restrict API modification of critical log data
        read_only_fields = ['id', 'created_at', 'error_message', 'endpoint_url', 'level']


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        min_length=2,
        error_messages={
            'invalid': _('Veuillez entrer une adresse e-mail valide.'),
            'blank': _('Ce champ est obligatoire.')
        }
    )


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        error_messages={
            'blank': _('Ce champ est obligatoire.')
        }
    )
    password_confirm = serializers.CharField(
        write_only=True,
        error_messages={
            'blank': _('Ce champ est obligatoire.')
        }
    )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        # 1. Check if passwords match
        if password != password_confirm:
            raise serializers.ValidationError({
                "password_confirm": _("Les mots de passe ne correspondent pas.")
            })

        # 2. Enforce Django's built-in password strength rules
        # (e.g., minimum length, not entirely numeric, etc.)
        try:
            validate_password(password)
        except DjangoValidationError as e:
            # Convert Django's validation errors into DRF validation errors
            raise serializers.ValidationError({
                "password": list(e.messages)
            })

        return attrs


class ProductImageExtractionSerializer(serializers.Serializer):
    image = serializers.ImageField(
        required=True,
        error_messages={
            'required': _("Une image est requise pour l'analyse."),
            'invalid': _("Le format de l'image est invalide.")
        }
    )

    def validate_image(self, value):
        # Validation stricte de la taille : 5 MB maximum
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(_("L'image ne doit pas dépasser 5 MB."))
        return value


class FinalDecisionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseIntention
        fields = ['user_final_decision']
        extra_kwargs = {
            'user_final_decision': {'required': True}
        }

    def validate_user_final_decision(self, value):
        # On s'assure que la décision fait partie des choix autorisés
        if value not in PurchaseIntention.DecisionChoices.values:
            raise serializers.ValidationError(_("Décision invalide."))
        return value


class AppFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppFeedback
        fields = ['id', 'user', 'rating', 'comment', 'created_at', 'subject']
        read_only_fields = ['id', 'user', 'created_at']

    def validate_rating(self, value):
        # Validation côté serveur de la note (1 à 5)
        if value < 1 or value > 5:
            raise serializers.ValidationError(_("La note doit être comprise entre 1 et 5 étoiles."))
        return value


# Partie administration
class AdminFeedbackSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = AppFeedback
        fields = ['id', 'user_email', 'subject', 'rating', 'comment', 'created_at']
