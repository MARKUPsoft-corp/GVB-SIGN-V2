from django.contrib import admin
from .models import DocumentSignature

@admin.register(DocumentSignature)
class DocumentSignatureAdmin(admin.ModelAdmin):
    list_display = [
        'original_filename', 'signer_full_name', 'user', 
        'signature_timestamp', 'created_at', 'is_verified'
    ]
    list_filter = [
        'signature_timestamp', 'created_at', 'user'
    ]
    search_fields = [
        'original_filename', 'signer_full_name', 'document_id', 'user__email'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'is_verified'
    ]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('id', 'document_id', 'original_filename', 'user', 'signer_full_name')
        }),
        ('Fichiers', {
            'fields': ('original_document', 'signed_document', 'file_size_original', 'file_size_signed')
        }),
        ('Signature', {
            'fields': ('document_hash', 'public_key', 'signature', 'signature_timestamp', 'execution_time')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at', 'is_verified'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')