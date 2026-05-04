# api/urls.py
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    GoogleLoginView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,

    UserProfileView, ExtractProductInfoView, PurchaseIntentionCreateView, GenerateQuestionsView, GenerateVerdictView,
    UserFinalDecisionView, DashboardSummaryView, AppFeedbackCreateView, PurchaseHistoryView, AdminFeedbackListView,
    PurchaseIntentionDetailView, StatsDashboardAPIView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/google/', GoogleLoginView.as_view(), name='google-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password-reset/', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('auth/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(),
         name='password-reset-confirm'),
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
    path('purchase-intentions/extract/', ExtractProductInfoView.as_view(), name='extract-product-info'),
    path('purchase-intentions/', PurchaseIntentionCreateView.as_view(), name='create-purchase-intention'),
    path('purchase-intentions/<uuid:intention_id>/generate-questions/',
         GenerateQuestionsView.as_view(), name='generate-questions'),
    path('purchase-intentions/<uuid:intention_id>/verdict/',
         GenerateVerdictView.as_view(), name='generate-verdict'),
    path('purchase-intentions/<uuid:intention_id>/final-decision/',
         UserFinalDecisionView.as_view(), name='user-final-decision'),
    path('dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('app-feedback/', AppFeedbackCreateView.as_view(), name='app-feedback'),

    path('purchase-intentions/<uuid:intention_id>/generate-questions/',
         GenerateQuestionsView.as_view(),
         name='generate-questions'),

    # 2. Envoi des réponses et génération du verdict par l'IA
    path('purchase-intentions/<uuid:intention_id>/verdict/',
         GenerateVerdictView.as_view(),
         name='generate-verdict'),

    # 3. Enregistrement de la décision finale de l'utilisateur (Acheter/Attendre/Abandonner)
    path('purchase-intentions/<uuid:intention_id>/final-decision/',
         UserFinalDecisionView.as_view(),
         name='user-final-decision'),
    path('purchase-intentions/history/', PurchaseHistoryView.as_view(), name='purchase-history'),
    path('admin-api/feedbacks/', AdminFeedbackListView.as_view(), name='admin-feedbacks'),
    path('purchase-intentions/<uuid:intention_id>/', PurchaseIntentionDetailView.as_view(),
         name='purchase-intention-detail'),
    path('dashboard/stats/', StatsDashboardAPIView.as_view(), name='dashboard-stats'),
]
