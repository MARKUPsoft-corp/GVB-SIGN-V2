from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from organizations.models import Organization, OrganizationMember
import uuid
import json

User = get_user_model()

class DocumentSignature(models.Model):
    """
    Modèle pour enregistrer les informations de signature de documents
    """
    # Identifiants
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_id = models.CharField(max_length=255, help_text="ID du document généré côté frontend")
    
    # Lien avec la préparation de document (optionnel pour les signatures directes)
    document_preparation = models.ForeignKey('DocumentPreparation', on_delete=models.CASCADE, null=True, blank=True, related_name='final_signatures', help_text="Préparation de document associée (pour les workflows)")
    
    # Utilisateur qui a signé
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signatures')
    signer_full_name = models.CharField(max_length=255, help_text="Nom complet de la personne qui a signé")
    
    # Fichiers
    original_document = models.FileField(upload_to='documents/original/', help_text="Document PDF original")
    signed_document = models.FileField(upload_to='documents/signed/', help_text="Document PDF signé")
    original_filename = models.CharField(max_length=255, help_text="Nom original du fichier")
    
    # Informations de signature
    document_hash = models.TextField(help_text="Hash SHA-256 du document original")
    public_key = models.TextField(help_text="Clé publique du certificat utilisé")
    signature = models.TextField(help_text="Signature numérique du document")
    
    # Métadonnées
    signature_timestamp = models.DateTimeField(help_text="Timestamp de la signature")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Informations supplémentaires
    file_size_original = models.PositiveIntegerField(help_text="Taille du fichier original en octets")
    file_size_signed = models.PositiveIntegerField(help_text="Taille du fichier signé en octets")
    execution_time = models.FloatField(help_text="Temps d'exécution de la signature en secondes")
    
    # Informations sur l'organisation (pour les workflows)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='document_signatures', help_text="Organisation associée")
    workflow_history = models.JSONField(default=list, help_text="Historique complet du workflow de signature")
    is_workflow_document = models.BooleanField(default=False, help_text="Indique si ce document provient d'un workflow organisationnel")
    
    class Meta:
        verbose_name = "Signature de document"
        verbose_name_plural = "Signatures de documents"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['document_id']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['signature_timestamp']),
        ]
    
    def __str__(self):
        return f"Signature de {self.original_filename} par {self.signer_full_name}"
    
    @property
    def is_verified(self):
        """
        Propriété pour indiquer si la signature peut être vérifiée
        (logique de vérification à implémenter si nécessaire)
        """
        return bool(self.signature and self.public_key and self.document_hash)


class DocumentPreparation(models.Model):
    """
    Modèle pour gérer le workflow de préparation et de signature hiérarchique des documents
    """
    
    # Statuts possibles du document dans le workflow
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('prepared', 'Préparé par le secrétaire'),
        ('pending_signature', 'En attente de signature'),
        ('in_progress', 'En cours de signature'),
        ('completed', 'Signé par tous'),
        ('rejected', 'Rejeté'),
        ('cancelled', 'Annulé'),
    ]
    
    # Identifiants
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_id = models.CharField(max_length=255, unique=True, help_text="ID unique du document")
    
    # Relations
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='document_preparations')
    prepared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prepared_documents', help_text="Secrétaire qui a préparé le document")
    current_signer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pending_documents', help_text="Personne qui doit signer actuellement")
    
    # Informations du document
    original_filename = models.CharField(max_length=255, help_text="Nom original du fichier")
    document_title = models.CharField(max_length=255, help_text="Titre du document")
    document_description = models.TextField(blank=True, help_text="Description du document")
    
    # Fichiers
    original_document = models.FileField(upload_to='documents/preparation/original/', help_text="Document PDF original")
    current_document = models.FileField(upload_to='documents/preparation/current/', help_text="Document PDF actuel (avec signatures partielles)")
    final_document = models.FileField(upload_to='documents/preparation/final/', null=True, blank=True, help_text="Document PDF final complètement signé")
    generated_pdf = models.FileField(upload_to='documents/preparation/generated/', null=True, blank=True, help_text="PDF généré avec les éléments positionnés")
    
    # Image de signature
    secretary_signature_image = models.ImageField(upload_to='signatures/secretary/', null=True, blank=True, help_text="Image de signature du secrétaire")
    
    # Configuration des éléments - QR Code
    qr_code_x = models.FloatField(null=True, blank=True, help_text="Position X du QR code")
    qr_code_y = models.FloatField(null=True, blank=True, help_text="Position Y du QR code")
    qr_code_size = models.CharField(max_length=10, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], null=True, blank=True, help_text="Taille du QR code")
    qr_code_page = models.PositiveIntegerField(default=1, help_text="Page du QR code")
    
    # Configuration des éléments - Signature
    signature_x = models.FloatField(null=True, blank=True, help_text="Position X de la signature")
    signature_y = models.FloatField(null=True, blank=True, help_text="Position Y de la signature")
    signature_width = models.FloatField(null=True, blank=True, help_text="Largeur de la signature")
    signature_height = models.FloatField(null=True, blank=True, help_text="Hauteur de la signature")
    signature_page = models.PositiveIntegerField(default=1, help_text="Page de la signature")
    
    # Configuration complète (pour compatibilité)
    elements_configuration = models.JSONField(default=dict, help_text="Configuration complète des éléments (JSON)")
    
    # Workflow et signatures
    signature_workflow = models.JSONField(default=list, help_text="Ordre des signataires dans le workflow")
    current_step = models.PositiveIntegerField(default=0, help_text="Étape actuelle dans le workflow (0 = préparation)")
    total_steps = models.PositiveIntegerField(default=0, help_text="Nombre total d'étapes dans le workflow")
    
    # Statut et métadonnées
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prepared_at = models.DateTimeField(null=True, blank=True, help_text="Date de préparation par le secrétaire")
    completed_at = models.DateTimeField(null=True, blank=True, help_text="Date de finalisation complète")
    
    # Informations supplémentaires
    file_size_original = models.PositiveIntegerField(default=0, help_text="Taille du fichier original en octets")
    preparation_notes = models.TextField(blank=True, help_text="Notes de préparation du secrétaire")
    rejection_reason = models.TextField(blank=True, help_text="Raison du rejet si applicable")
    
    class Meta:
        verbose_name = "Préparation de document"
        verbose_name_plural = "Préparations de documents"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['document_id']),
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['prepared_by', 'created_at']),
            models.Index(fields=['current_signer', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"Préparation: {self.document_title} - {self.organization.name}"
    
    @property
    def progress_percentage(self):
        """Calcule le pourcentage de progression du workflow"""
        if self.total_steps == 0:
            return 0
        return int((self.current_step / self.total_steps) * 100)
    
    @property
    def is_completed(self):
        """Vérifie si le document est complètement signé"""
        return self.status == 'completed'
    
    @property
    def next_signer_info(self):
        """Retourne les informations du prochain signataire"""
        if self.current_step < len(self.signature_workflow):
            signer_data = self.signature_workflow[self.current_step]
            return signer_data
        return None
    
    def get_signature_history(self):
        """Retourne l'historique des signatures pour ce document"""
        return DocumentSignatureStep.objects.filter(
            document_preparation=self
        ).order_by('step_order')
    
    def advance_workflow(self):
        """Avance le workflow à l'étape suivante"""
        if self.current_step < self.total_steps:
            self.current_step += 1
            if self.current_step >= self.total_steps:
                self.status = 'completed'
                self.completed_at = timezone.now()
            else:
                # Définir le prochain signataire
                next_signer_info = self.next_signer_info
                if next_signer_info:
                    try:
                        self.current_signer = User.objects.get(id=next_signer_info['user_id'])
                    except User.DoesNotExist:
                        pass
            self.save()


class DocumentSignatureStep(models.Model):
    """
    Modèle pour enregistrer chaque étape de signature dans le workflow
    """
    
    # Relations
    document_preparation = models.ForeignKey(DocumentPreparation, on_delete=models.CASCADE, related_name='signature_steps')
    signer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signature_steps')
    organization_member = models.ForeignKey(OrganizationMember, on_delete=models.CASCADE, related_name='signature_steps')
    
    # Informations de l'étape
    step_order = models.PositiveIntegerField(help_text="Ordre de cette étape dans le workflow")
    signer_name = models.CharField(max_length=255, help_text="Nom complet du signataire")
    signer_role = models.CharField(max_length=50, help_text="Rôle du signataire dans l'organisation")
    signer_email = models.EmailField(help_text="Email du signataire")
    
    # Signature
    signature_image = models.TextField(blank=True, help_text="Image de la signature (base64)")
    signature_position = models.JSONField(default=dict, help_text="Position de la signature sur le document")
    digital_signature = models.TextField(blank=True, help_text="Signature numérique cryptographique")
    public_key = models.TextField(blank=True, help_text="Clé publique utilisée pour la signature")
    
    # Métadonnées
    signed_at = models.DateTimeField(null=True, blank=True, help_text="Date et heure de signature")
    signature_hash = models.TextField(blank=True, help_text="Hash de la signature")
    document_hash_at_signing = models.TextField(blank=True, help_text="Hash du document au moment de la signature")
    
    # Statut de l'étape
    is_completed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, help_text="Raison du rejet si applicable")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Étape de signature"
        verbose_name_plural = "Étapes de signature"
        ordering = ['document_preparation', 'step_order']
        unique_together = ['document_preparation', 'step_order']
        indexes = [
            models.Index(fields=['document_preparation', 'step_order']),
            models.Index(fields=['signer', 'is_completed']),
            models.Index(fields=['signed_at']),
        ]
    
    def __str__(self):
        status = "Signé" if self.is_completed else ("Rejeté" if self.is_rejected else "En attente")
        return f"Étape {self.step_order}: {self.signer_name} ({self.signer_role}) - {status}"