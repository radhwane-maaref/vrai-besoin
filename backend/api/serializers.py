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
            'financial_goal', 'location_data', 'auth_provider'
        ]
        extra_kwargs = {
            'email': {'read_only': True},
            'username': {'read_only': True}
        }


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

    class Meta:
        model = CustomUser
        # On inclut l'email, le mot de passe et les champs optionnels
        fields = ['email', 'password', 'monthly_budget', 'profession']
        extra_kwargs = {
            'email': {
                'required': True,
                'error_messages': {
                    'blank': _("L'adresse e-mail est obligatoire."),
                    'invalid': _("Veuillez entrer une adresse e-mail valide.")
                }
            }
        }

    def create(self, validated_data):
        # Hachage sécurisé du mot de passe avant l'enregistrement dans PostgreSQL
        validated_data['password'] = make_password(validated_data.get('password'))

        # Création de l'utilisateur avec les données validées et sécurisées
        return super().create(validated_data)

class ReflectionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReflectionQuestion
        fields = ['id', 'purchase_intention', 'question_text', 'user_answer']

class PurchaseIntentionSerializer(serializers.ModelSerializer):
    # Matches the related_name='questions' in the ReflectionQuestion model
    questions = ReflectionQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseIntention
        fields = [
            'id', 'user', 'product_name', 'product_price', 'product_category',
            'product_image', 'ai_verdict', 'ai_reasoning', 'user_final_decision',
            'created_at', 'updated_at', 'questions'
        ]

class AppFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppFeedback
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(_("La note doit être comprise entre 1 et 5 étoiles."))
        return value

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