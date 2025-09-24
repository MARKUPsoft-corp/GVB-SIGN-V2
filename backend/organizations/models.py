from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import timedelta
import json

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
        count = self.members.filter(role='admin').count()
        print(f"🔍 Admin count pour {self.name}: {count}")
        print(f"🔍 Tous les membres: {list(self.members.values('user__email', 'role'))}")
        return count

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


class DemandeAdhesion(models.Model):
    """
    Modèle pour gérer les demandes d'adhésion aux organisations
    """
    # Utilisateur qui fait la demande
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership_requests', verbose_name="Utilisateur")
    
    # Organisation demandée
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='membership_requests', verbose_name="Organisation")
    
    # Rôle souhaité par l'utilisateur
    requested_role = models.CharField(max_length=50, choices=[
        ('secretaire', 'Secrétaire'),
        ('chef', 'Chef'),
        ('chef+1', 'Chef+1'),
        ('chef+2', 'Chef+2'),
        ('chef+n', 'Chef+n'),
    ], verbose_name="Rôle souhaité")
    
    # Code d'invitation généré pour cette demande
    invitation_code = models.OneToOneField(InvitationCode, on_delete=models.CASCADE, related_name='membership_request', verbose_name="Code d'invitation")
    
    # Statut de la demande
    status = models.CharField(max_length=20, choices=[
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),
        ('rejected', 'Rejetée'),
        ('cancelled', 'Annulée'),
    ], default='pending', verbose_name="Statut")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de traitement")
    
    # Utilisateur qui a traité la demande (admin de l'organisation)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_membership_requests', verbose_name="Traité par")
    
    # Message de l'utilisateur (optionnel)
    message = models.TextField(blank=True, null=True, verbose_name="Message")
    
    # Réponse de l'organisation (optionnel)
    response_message = models.TextField(blank=True, null=True, verbose_name="Message de réponse")
    
    class Meta:
        verbose_name = "Demande d'adhésion"
        verbose_name_plural = "Demandes d'adhésion"
        db_table = 'organizations_membership_request'
        ordering = ['-created_at']
        unique_together = ['user', 'organization']  # Un utilisateur ne peut faire qu'une demande par organisation
    
    def __str__(self):
        return f"{self.user.full_name} → {self.organization.name} ({self.get_requested_role_display()})"
    
    def approve(self, processed_by_user, response_message=None):
        """Approuve la demande d'adhésion"""
        self.status = 'approved'
        self.processed_by = processed_by_user
        self.processed_at = timezone.now()
        self.response_message = response_message
        self.save()
        
        # Réactiver le code d'invitation s'il était désactivé (cas de réapprobation)
        if not self.invitation_code.is_active:
            self.invitation_code.is_active = True
            self.invitation_code.save()
        
        # Si le code était déjà utilisé (cas de réapprobation), créer directement l'adhésion
        if self.invitation_code.is_used:
            # Vérifier si l'utilisateur n'est pas déjà membre
            if not OrganizationMember.objects.filter(
                organization=self.invitation_code.organization,
                user=self.user
            ).exists():
                OrganizationMember.objects.create(
                    organization=self.invitation_code.organization,
                    user=self.user,
                    role=self.invitation_code.role,
                    invited_by=self.invitation_code.created_by
                )
        else:
            # Utiliser le code d'invitation normalement
            self.invitation_code.use_code(self.user)
    
    def reject(self, processed_by_user, response_message=None):
        """Rejette la demande d'adhésion"""
        self.status = 'rejected'
        self.processed_by = processed_by_user
        self.processed_at = timezone.now()
        self.response_message = response_message
        self.save()
        
        # Désactiver le code d'invitation
        self.invitation_code.is_active = False
        self.invitation_code.save()
    
    def cancel(self):
        """Annule la demande d'adhésion"""
        self.status = 'cancelled'
        self.processed_at = timezone.now()
        self.save()
        
        # Désactiver le code d'invitation
        self.invitation_code.is_active = False
        self.invitation_code.save()


# Signal pour réactiver automatiquement les codes d'invitation quand un membre quitte l'organisation
@receiver(post_delete, sender=OrganizationMember)
def reactivate_invitation_codes(sender, instance, **kwargs):
    """
    Réactive automatiquement les codes d'invitation quand un membre quitte l'organisation
    """
    try:
        # Trouver tous les codes d'invitation utilisés par cet utilisateur pour cette organisation
        invitation_codes = InvitationCode.objects.filter(
            organization=instance.organization,
            used_by=instance.user,
            is_used=True
        )
        
        for invitation_code in invitation_codes:
            # Réactiver le code d'invitation
            invitation_code.is_used = False
            invitation_code.used_by = None
            invitation_code.used_at = None
            invitation_code.save()
            print(f"✅ Code d'invitation {invitation_code.code} automatiquement réactivé")
            
    except Exception as e:
        print(f"❌ Erreur lors de la réactivation automatique des codes: {str(e)}")


class OrganizationCertificate(models.Model):
    """
    Modèle pour stocker les certificats d'organisation
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=255, help_text="Nom du certificat")
    subject_common_name = models.CharField(max_length=255, blank=True, null=True)
    subject_organization = models.CharField(max_length=255, blank=True, null=True)
    subject_organizational_unit = models.CharField(max_length=255, blank=True, null=True)
    subject_country = models.CharField(max_length=10, blank=True, null=True)
    subject_email = models.EmailField(blank=True, null=True)
    
    issuer_common_name = models.CharField(max_length=255, blank=True, null=True)
    issuer_organization = models.CharField(max_length=255, blank=True, null=True)
    issuer_country = models.CharField(max_length=10, blank=True, null=True)
    
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    fingerprint = models.CharField(max_length=255, blank=True, null=True)
    signature_algorithm = models.CharField(max_length=100, blank=True, null=True)
    
    not_before = models.DateTimeField(blank=True, null=True)
    not_after = models.DateTimeField(blank=True, null=True)
    is_valid = models.BooleanField(default=True)
    
    # Clés cryptographiques (stockées de manière sécurisée)
    private_key_pem = models.TextField(blank=True, null=True, help_text="Clé privée au format PEM")
    public_key_pem = models.TextField(blank=True, null=True, help_text="Clé publique au format PEM")
    certificate_pem = models.TextField(blank=True, null=True, help_text="Certificat au format PEM")
    
    # Métadonnées
    key_usage = models.JSONField(default=list, blank=True, help_text="Usages de clé autorisés")
    imported_at = models.DateTimeField(auto_now_add=True)
    imported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imported_certificates')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Certificat d'organisation"
        verbose_name_plural = "Certificats d'organisation"
        ordering = ['-imported_at']
    
    def __str__(self):
        return f"{self.name} - {self.organization.name}"
    
    @property
    def is_expired(self):
        """Vérifie si le certificat est expiré"""
        if not self.not_after:
            return False
        return timezone.now() > self.not_after
    
    @property
    def days_until_expiry(self):
        """Retourne le nombre de jours avant expiration"""
        if not self.not_after:
            return None
        delta = self.not_after - timezone.now()
        return delta.days if delta.days > 0 else 0
    
    def get_subject_info(self):
        """Retourne les informations du sujet sous forme de dictionnaire"""
        return {
            'commonName': self.subject_common_name,
            'organization': self.subject_organization,
            'organizationalUnit': self.subject_organizational_unit,
            'country': self.subject_country,
            'email': self.subject_email
        }
    
    def get_issuer_info(self):
        """Retourne les informations de l'émetteur sous forme de dictionnaire"""
        return {
            'commonName': self.issuer_common_name,
            'organization': self.issuer_organization,
            'country': self.issuer_country
        }
    
    def get_validity_info(self):
        """Retourne les informations de validité"""
        return {
            'notBefore': self.not_before.isoformat() if self.not_before else None,
            'notAfter': self.not_after.isoformat() if self.not_after else None,
            'isValid': self.is_valid and not self.is_expired,
            'isExpired': self.is_expired,
            'daysUntilExpiry': self.days_until_expiry
        }