import uuid
import sys
from io import BytesIO
from PIL import Image

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


# les classes de mon application

class CustomUserManager(BaseUserManager):
    """
    Manager personnalisé pour utiliser l'email comme identifiant principal
    à la place du username.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("L'adresse e-mail est obligatoire."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


# L'utilisateur personalisé
class CustomUser(AbstractUser):
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    profession = models.CharField(max_length=150, null=True, blank=True)
    financial_goal = models.TextField(null=True, blank=True)
    last_ip_address = models.GenericIPAddressField(null=True, blank=True)
    location_data = models.JSONField(default=dict, blank=True)
    cooldown_preference = models.IntegerField(
        default=24,
        help_text=_("Temps de réflexion par défaut en heures (12, 24, 48, 72)")
    )
    preferred_currency = models.CharField(max_length=3, default='TND')
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class AuthProviders(models.TextChoices):
        EMAIL = 'EMAIL', _('Email')
        GOOGLE = 'GOOGLE', _('Google')

    class RigorChoices(models.TextChoices):
        INDULGENT = 'Indulgent', _('Indulgent')
        BALANCED = 'Équilibré', _('Équilibré')
        RUTHLESS = 'Impitoyable', _('Impitoyable')

    evaluation_rigor = models.CharField(
        max_length=20,
        choices=RigorChoices.choices,
        default=RigorChoices.BALANCED,
        help_text=_("Niveau de rigueur du coach IA")
    )
    auth_provider = models.CharField(
        max_length=10,
        choices=AuthProviders.choices,
        default=AuthProviders.EMAIL,
        help_text=_("Méthode d'inscription utilisée par l'utilisateur")
    )
    google_id = models.CharField(max_length=255, null=True, blank=True, unique=True)

    def delete(self, *args, **kwargs):
        # Désactive le compte au lieu de le supprimer ( Soft delete )
        self.is_active = False
        self.save()

    def __str__(self):
        return self.email or self.username


class PurchaseIntention(models.Model):
    class DecisionChoices(models.TextChoices):
        BUY = 'BUY', _('Acheter')
        CALM_DOWN = 'CALM', _('Calm Down (Réflexion)')
        ABANDON = 'ABANDON', _('Abandonner')
        UNKOWN = 'UNKOWN', _('Inconnu')

    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                             blank=True, related_name='purchase_intentions')
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_category = models.CharField(max_length=100)
    usage_frequency = models.CharField(max_length=50, null=True, blank=True)
    has_similar_item = models.BooleanField(default=False)
    urgency_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=3)
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_incoherent_bypassed = models.BooleanField(
        default=False,
        help_text=_("Indique si l'utilisateur a forcé la création malgré l'alerte d'incohérence")
    )
    ai_verdict = models.CharField(
        max_length=10,
        choices=DecisionChoices.choices,
        null=True,
        blank=True,
        help_text=_("Le verdict rendu par l'IA")
    )
    ai_reasoning = models.TextField(null=True, blank=True,
                                    help_text=_("L'argumentaire généré par l'IA pour justifier son verdict"))
    user_final_decision = models.CharField(
        max_length=10,
        choices=DecisionChoices.choices,
        default=DecisionChoices.UNKOWN,
        null=True,
        blank=True,
        help_text=_("La décision finale prise par l'utilisateur")
    )
    cooldown_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Date d'expiration de la période de réflexion")
    )

    def save(self, *args, **kwargs):
        # Image compression logic
        if self.product_image:
            # Check if this is a new image or just updating the model
            # We don't want to re-compress an already compressed image
            is_new_image = False
            if not self.pk:
                is_new_image = True
            else:
                orig = PurchaseIntention.objects.get(pk=self.pk)
                if orig.product_image != self.product_image:
                    is_new_image = True

            if is_new_image:
                try:
                    # Open the image using Pillow
                    img = Image.open(self.product_image)

                    # Convert to RGB if necessary (e.g., for PNGs with transparency)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")

                    # Resize if the image is too large (e.g., max width/height of 1024)
                    max_size = (1024, 1024)
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)

                    # Save the compressed image to a BytesIO object
                    output = BytesIO()
                    img.save(output, format='JPEG', quality=75, optimize=True)
                    output.seek(0)

                    # Replace the original uploaded file with the compressed one
                    self.product_image = InMemoryUploadedFile(
                        output,
                        'ImageField',
                        f"{self.product_image.name.split('.')[0]}.jpg",
                        'image/jpeg',
                        sys.getsizeof(output),
                        None
                    )
                except Exception as e:
                    # Log the error but don't stop the save process
                    # You might want to use your ErrorLog model here in a real app
                    print(f"Error compressing image: {e}")

        super().save(*args, **kwargs)


class ReflectionQuestion(models.Model):
    purchase_intention = models.ForeignKey(PurchaseIntention, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=300)
    # La question generé par l'IA
    question_text = models.CharField(max_length=300)

    ai_options = models.JSONField(default=list, blank=True, null=True)
    # La réponse de l'utilisateur
    user_answer = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Vérification de la limite de 3 questions par intention d'achat
        # On ne fait le test que lors de la création initiale (quand il n'y a pas encore de primary key 'pk')
        if not self.pk:
            existing_questions_count = ReflectionQuestion.objects.filter(
                purchase_intention=self.purchase_intention
            ).count()

            if existing_questions_count >= 3:
                raise ValidationError(_("Une intention d'achat ne peut pas avoir plus de 3 questions de réflexion."))

        # Si la vérification passe, on sauvegarde normalement
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Q: {self.question_text[:50]}..."


class AppFeedback(models.Model):
    # Ici l'idée est de garder l'avis de l'utilisateur meme s'il a supprimé son compte
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                 help_text=_("Note de 1 à 5 étoiles"))
    subject = models.CharField(max_length=255, null=True, blank=True, help_text=_("Objet du message"))
    comment = models.TextField(null=True, blank=True, help_text=_("Commentaire facultatif"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de {self.user} - {self.subject or 'Sans objet'}"


class ErrorLog(models.Model):
    class LogLevels(models.TextChoices):
        WARNING = 'WARN', _('Avertissement')
        ERROR = 'ERROR', _('Erreur')
        CRITICAL = 'CRIT', _('Critique (Crash)')

    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    level = models.CharField(max_length=5, choices=LogLevels.choices, default=LogLevels.ERROR)

    # Le message d'erreur technique (ex: l'erreur Python ou API renvoyée)
    error_message = models.TextField()

    # Savoir à quel moment et sur quelle page ça s'est produit
    endpoint_url = models.CharField(max_length=255, null=True, blank=True,
                                    help_text=_("L'URL de l'API où l'erreur s'est produite"))

    # Lien avec l'utilisateur si possible (pour l'aider s'il appelle le support)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    is_resolved = models.BooleanField(default=False, help_text=_("Indique si le développeur a corrigé ce bug"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.level}] {self.endpoint_url} - Résolu: {self.is_resolved}"


class SavingsGoal(models.Model):
    """
    Objectif d'épargne de l'utilisateur.
    On le sépare de CustomUser pour pouvoir en avoir plusieurs dans le futur (historique).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='savings_goals'
    )
    goal_name = models.CharField(max_length=150, help_text=_("Ex: Nouvel Ordinateur"))
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    saved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.goal_name} - {self.user.email}"
