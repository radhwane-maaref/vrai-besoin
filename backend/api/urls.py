# api/urls.py
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    GoogleLoginView,
    PasswordResetConfirmAPIView,

    UserProfileView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/google/', GoogleLoginView.as_view(), name='google-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password-reset/', PasswordResetConfirmAPIView.as_view(), name='password-reset-request'),
    path('auth/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
]
