# api/services.py
import os
from google.oauth2 import id_token
from google.auth.transport import requests
from django.core.mail import send_mail
from django.conf import settings


def verify_google_token(token: str) -> dict:
    """Verifies the Google JWT and extracts user info."""
    try:
        # Client ID should be loaded from .env via settings
        client_id = settings.GOOGLE_OAUTH_CLIENT_ID
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)
        return idinfo
    except ValueError:
        return None


def send_password_reset_email(email: str, reset_url: str):
    """Sends the reset email via Brevo (configured as SMTP in settings.py)."""
    subject = "Vrai Besoin - Réinitialisation de votre mot de passe"
    message = f"Bonjour,\n\nVous avez demandé la réinitialisation de votre mot de passe. Cliquez sur le lien suivant : {reset_url}\n\nSi vous n'êtes pas à l'origine de cette demande, ignorez cet e-mail."

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )