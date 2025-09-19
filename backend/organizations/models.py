from django.db import models
from django.contrib.auth import get_user_model

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
        ('member', 'Membre'),
        ('viewer', 'Observateur'),
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