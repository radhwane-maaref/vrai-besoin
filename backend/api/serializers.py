from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, PurchaseIntention, ReflectionQuestion, AppFeedback, ErrorLog

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