from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class DocumentSignature(models.Model):
    """
    Modèle pour enregistrer les informations de signature de documents
    """
    # Identifiants
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_id = models.CharField(max_length=255, help_text="ID du document généré côté frontend")
    
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