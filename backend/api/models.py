import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
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
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    class AuthProviders(models.TextChoices):
        EMAIL = 'EMAIL', _('Email')
        GOOGLE = 'GOOGLE', _('Google')

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
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
        null=True,
        blank=True,
        help_text=_("La décision finale prise par l'utilisateur")
    )


class ReflectionQuestion(models.Model):
    class AnswerChoices(models.TextChoices):
        YES = 'YES', _('Oui')
        NO = 'NO', _('Non')
        IDK = 'IDK', _('Je ne sais pas')

    purchase_intention = models.ForeignKey(PurchaseIntention, on_delete=models.CASCADE, related_name="questions")

    # La question generé par l'IA
    question_text = models.CharField(max_length=300)
    # La réponse de l'utilisateur
    user_answer = models.CharField(
        max_length=3,
        choices=AnswerChoices.choices,
        null=True,
        blank=True)

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
    comment = models.TextField(null=True, blank=True, help_text=_("Commentaire facultatif"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de {self.user} - {self.rating} Etoiles"


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
