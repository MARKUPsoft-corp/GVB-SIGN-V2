from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Organization(models.Model):
    """
    Modèle pour les organisations
    """
    name = models.CharField(max_length=200, verbose_name="Nom de l'organisation")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    email = models.EmailField(verbose_name="Email de contact")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    address = models.TextField(blank=True, null=True, verbose_name="Adresse")
    website = models.URLField(blank=True, null=True, verbose_name="Site web")
    organization_type = models.CharField(max_length=50, choices=[
        ('entreprise', 'Entreprise'),
        ('association', 'Association'),
        ('administration', 'Administration'),
        ('collectivite', 'Collectivité'),
        ('autre', 'Autre'),
    ], verbose_name="Type d'organisation")
    sector = models.CharField(max_length=100, blank=True, null=True, verbose_name="Secteur d'activité")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_organizations', verbose_name="Créé par")
    
    # Statut de l'organisation
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_approved = models.BooleanField(default=False, verbose_name="Approuvée par l'admin")
    approval_date = models.DateTimeField(blank=True, null=True, verbose_name="Date d'approbation")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='approved_organizations', verbose_name="Approuvée par")
    
    class Meta:
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"
        db_table = 'organizations_organization'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def admin_count(self):
        """Retourne le nombre d'administrateurs de l'organisation"""
        return self.members.filter(role='admin').count()

    @property
    def member_count(self):
        """Retourne le nombre total de membres de l'organisation"""
        return self.members.count()


class OrganizationMember(models.Model):
    """
    Modèle pour gérer les membres d'une organisation
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members', verbose_name="Organisation")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization_memberships', verbose_name="Utilisateur")
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Administrateur'),
        ('secretaire', 'Secrétaire'),
        ('chef', 'Chef'),
        ('chef+1', 'Chef+1'),
        ('chef+2', 'Chef+2'),
        ('chef+n', 'Chef+n'),
    ], default='member', verbose_name="Rôle")
    
    # Métadonnées
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'adhésion")
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='invited_members', verbose_name="Invité par")
    
    class Meta:
        verbose_name = "Membre d'organisation"
        verbose_name_plural = "Membres d'organisation"
        db_table = 'organizations_member'
        unique_together = ['organization', 'user']
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.organization.name} ({self.get_role_display()})"


class InvitationCode(models.Model):
    """
    Modèle pour gérer les codes d'invitation aux organisations
    """
    # Code d'invitation unique
    code = models.CharField(max_length=100, unique=True, verbose_name="Code d'invitation")
    
    # Organisation liée
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='invitation_codes', verbose_name="Organisation")
    
    # Rôle attribué lors de l'acceptation
    role = models.CharField(max_length=50, choices=[
        ('secretaire', 'Secrétaire'),
        ('chef', 'Chef'),
        ('chef+1', 'Chef+1'),
        ('chef+2', 'Chef+2'),
        ('chef+n', 'Chef+n'),
    ], verbose_name="Rôle attribué")
    
    # Utilisateur qui a créé l'invitation
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_invitations', verbose_name="Créé par")
    
    # Utilisateur qui a utilisé l'invitation (null si pas encore utilisé)
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='used_invitations', verbose_name="Utilisé par")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    expires_at = models.DateTimeField(verbose_name="Date d'expiration")
    used_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'utilisation")
    
    # Statut
    is_active = models.BooleanField(default=True, verbose_name="Code actif")
    is_used = models.BooleanField(default=False, verbose_name="Code utilisé")
    
    class Meta:
        verbose_name = "Code d'invitation"
        verbose_name_plural = "Codes d'invitation"
        db_table = 'organizations_invitation_code'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.organization.name} ({self.get_role_display()})"
    
    def save(self, *args, **kwargs):
        """Sauvegarde avec expiration automatique à 7 jours"""
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        """Vérifie si le code a expiré"""
        return timezone.now() > self.expires_at
    
    @property
    def is_valid(self):
        """Vérifie si le code est valide (actif, non utilisé, non expiré)"""
        return self.is_active and not self.is_used and not self.is_expired
    
    def use_code(self, user):
        """Marque le code comme utilisé par un utilisateur"""
        if not self.is_valid:
            raise ValueError("Le code d'invitation n'est pas valide")
        
        self.used_by = user
        self.used_at = timezone.now()
        self.is_used = True
        self.save()
        
        # Créer l'adhésion à l'organisation
        OrganizationMember.objects.create(
            organization=self.organization,
            user=user,
            role=self.role,
            invited_by=self.created_by
        )