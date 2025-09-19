from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Gestionnaire d'utilisateur personnalisé pour utiliser l'email comme identifiant
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        email = self.normalize_email(email)
        
        # Générer un username unique basé sur l'email
        username = email.split('@')[0]
        counter = 1
        original_username = username
        
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1
            
        extra_fields.setdefault('username', username)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé pour GVB Sign
    """
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=150, verbose_name="Prénom")
    last_name = models.CharField(max_length=150, verbose_name="Nom")
    is_verified = models.BooleanField(default=False, verbose_name="Email vérifié")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    # Champs pour les organisations
    organization = models.ForeignKey('organizations.Organization', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Organisation")
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Administrateur'),
        ('member', 'Membre'),
        ('viewer', 'Observateur'),
    ], default='member', verbose_name="Rôle")

    # Utiliser l'email comme nom d'utilisateur
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        db_table = 'auth_user'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        return f"{self.first_name} {self.last_name}".strip()