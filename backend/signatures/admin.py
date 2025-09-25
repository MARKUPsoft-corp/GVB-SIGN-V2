from django.contrib import admin
from django.utils.html import format_html, escape
from django.utils.safestring import mark_safe
from django.utils import timezone
import json
from .models import DocumentSignature, DocumentPreparation, DocumentSignatureStep

@admin.register(DocumentSignature)
class DocumentSignatureAdmin(admin.ModelAdmin):
    list_display = [
        'original_filename', 'signer_full_name', 'user', 'organization',
        'is_workflow_document', 'signature_timestamp', 'created_at', 'is_verified'
    ]
    list_filter = [
        'signature_timestamp', 'created_at', 'user', 'organization', 'is_workflow_document'
    ]
    search_fields = [
        'original_filename', 'signer_full_name', 'document_id', 'user__email'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'is_verified'
    ]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('id', 'document_id', 'original_filename', 'user', 'signer_full_name', 'document_preparation')
        }),
        ('Organisation et Workflow', {
            'fields': ('organization', 'is_workflow_document', 'workflow_history')
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
        return super().get_queryset(request).select_related('user', 'organization', 'document_preparation')


@admin.register(DocumentPreparation)
class DocumentPreparationAdmin(admin.ModelAdmin):
    list_display = ['document_title', 'organization', 'prepared_by', 'current_signer', 'status', 'page_mode', 'progress_display', 'has_qr_config', 'has_signature_config', 'has_signature_image', 'has_generated_pdf', 'created_at']
    list_filter = ['status', 'organization', 'created_at', 'prepared_at']
    search_fields = ['document_title', 'document_id', 'original_filename', 'prepared_by__first_name', 'prepared_by__last_name']
    readonly_fields = ['id', 'progress_percentage', 'elements_config_display', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('id', 'document_id', 'document_title', 'document_description', 'original_filename')
        }),
        ('Organisation et Workflow', {
            'fields': ('organization', 'prepared_by', 'current_signer', 'signature_workflow')
        }),
        ('Progression', {
            'fields': ('status', 'current_step', 'total_steps', 'progress_percentage')
        }),
        ('Fichiers', {
            'fields': ('original_document', 'current_document', 'final_document', 'generated_pdf')
        }),
        ('Mode d\'application', {
            'fields': ('page_mode', 'applied_pages'),
            'description': 'Mode d\'application des éléments et pages concernées'
        }),
        ('Configuration QR Code', {
            'fields': ('qr_code_x', 'qr_code_y', 'qr_code_size'),
            'classes': ('collapse',)
        }),
        ('Configuration Signature', {
            'fields': ('signature_x', 'signature_y', 'signature_width', 'signature_height', 'secretary_signature_image'),
            'classes': ('collapse',)
        }),
        ('Configuration complète (JSON)', {
            'fields': ('elements_configuration', 'elements_config_display'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('file_size_original', 'preparation_notes', 'rejection_reason', 'prepared_at', 'completed_at', 'created_at', 'updated_at')
        }),
    )
    
    def progress_display(self, obj):
        """Affiche une barre de progression visuelle"""
        percentage = obj.progress_percentage
        color = 'green' if percentage == 100 else 'orange' if percentage > 50 else 'red'
        return format_html(
            '<div style="width: 100px; background-color: #f0f0f0; border-radius: 3px;">'
            '<div style="width: {}%; background-color: {}; height: 20px; border-radius: 3px; text-align: center; color: white; font-size: 12px; line-height: 20px;">'
            '{}%</div></div>',
            percentage, color, percentage
        )
    progress_display.short_description = 'Progression'
    
    actions = ['mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{updated} préparation(s) marquée(s) comme complétée(s).')
    mark_as_completed.short_description = "Marquer comme complété"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} préparation(s) annulée(s).')
    mark_as_cancelled.short_description = "Annuler"
    
    def has_qr_config(self, obj):
        """Indique si le document a une configuration QR code"""
        return bool(obj.qr_code_x is not None and obj.qr_code_y is not None)
    has_qr_config.boolean = True
    has_qr_config.short_description = 'QR Code'
    
    def has_signature_config(self, obj):
        """Indique si le document a une configuration de signature"""
        return bool(obj.signature_x is not None and obj.signature_y is not None)
    has_signature_config.boolean = True
    has_signature_config.short_description = 'Signature'
    
    def has_signature_image(self, obj):
        """Indique si le document a une image de signature"""
        return bool(obj.secretary_signature_image)
    has_signature_image.boolean = True
    has_signature_image.short_description = 'Image signature'
    
    def has_generated_pdf(self, obj):
        """Indique si le document a un PDF généré"""
        return bool(obj.generated_pdf)
    has_generated_pdf.boolean = True
    has_generated_pdf.short_description = 'PDF généré'
    
    def elements_config_display(self, obj):
        """Affiche la configuration des éléments de manière lisible"""
        html_parts = []
        
        # Afficher le mode d'application et les pages
        mode_display = {
            'all': 'Toutes les pages',
            'current': 'Page actuelle',
            'custom': 'Pages personnalisées',
            'individual': 'Positions individuelles'
        }
        pages_info = ""
        if obj.applied_pages:
            if isinstance(obj.applied_pages, list) and obj.applied_pages:
                pages_info = f" | Pages: {', '.join(map(str, obj.applied_pages))}"
        
        mode_html = (
            '<div style="margin-bottom: 10px; padding: 8px; background: #fff3cd; border-radius: 4px; border-left: 4px solid #ffc107;">'
            '<strong>📋 Mode d\'application</strong><br>'
            f'{mode_display.get(obj.page_mode, obj.page_mode)}{pages_info}'
            '</div>'
        )
        html_parts.append(mark_safe(mode_html))
        
        # Afficher la configuration QR Code (depuis les champs séparés)
        if obj.qr_code_x is not None and obj.qr_code_y is not None:
            qr_html = (
                '<div style="margin-bottom: 10px; padding: 8px; background: #e8f4fd; border-radius: 4px; border-left: 4px solid #007bff;">'
                '<strong>📱 QR Code</strong><br>'
                f'Position: X={obj.qr_code_x}, Y={obj.qr_code_y} | Taille: {obj.qr_code_size or "medium"}'
                '</div>'
            )
            html_parts.append(mark_safe(qr_html))
        
        # Afficher la configuration Signature (depuis les champs séparés)
        if obj.signature_x is not None and obj.signature_y is not None:
            sig_html = (
                '<div style="margin-bottom: 10px; padding: 8px; background: #e8f5e8; border-radius: 4px; border-left: 4px solid #28a745;">'
                '<strong>🖊️ Signature manuscrite</strong><br>'
                f'Position: X={obj.signature_x}, Y={obj.signature_y} | Taille: {obj.signature_width or "N/A"}x{obj.signature_height or "N/A"}'
                '</div>'
            )
            html_parts.append(mark_safe(sig_html))
        
        # Afficher aussi la configuration JSON si elle existe
        if obj.elements_configuration:
            try:
                json_str = json.dumps(obj.elements_configuration, indent=2)
                # Utiliser mark_safe au lieu de format_html pour éviter les problèmes de template
                escaped_json = escape(json_str)
                json_html = (
                    '<div style="margin-bottom: 10px; padding: 8px; background: #f8f9fa; border-radius: 4px; border-left: 4px solid #6c757d;">'
                    '<strong>📄 Configuration JSON</strong><br>'
                    f'<pre style="font-size: 11px; margin: 5px 0; white-space: pre-wrap;">{escaped_json}</pre>'
                    '</div>'
                )
                html_parts.append(mark_safe(json_html))
            except Exception as e:
                error_html = (
                    '<div style="margin-bottom: 10px; padding: 8px; background: #fff3cd; border-radius: 4px; border-left: 4px solid #ffc107;">'
                    '<strong>⚠️ Erreur JSON</strong><br>'
                    f'Impossible d\'afficher la configuration: {escape(str(e))}'
                    '</div>'
                )
                html_parts.append(mark_safe(error_html))
        
        if not html_parts:
            return "Aucune configuration définie"
            
        return mark_safe(''.join(html_parts))
    elements_config_display.short_description = 'Configuration des éléments'


@admin.register(DocumentSignatureStep)
class DocumentSignatureStepAdmin(admin.ModelAdmin):
    list_display = ['document_preparation', 'step_order', 'signer_name', 'signer_role', 'status_display', 'signed_at']
    list_filter = ['is_completed', 'is_rejected', 'signer_role', 'signed_at', 'created_at']
    search_fields = ['signer_name', 'signer_email', 'document_preparation__document_title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('document_preparation', 'step_order')
        }),
        ('Signataire', {
            'fields': ('signer', 'organization_member', 'signer_name', 'signer_role', 'signer_email')
        }),
        ('Signature', {
            'fields': ('signature_image', 'signature_position', 'digital_signature', 'public_key')
        }),
        ('Statut', {
            'fields': ('is_completed', 'is_rejected', 'rejection_reason', 'signed_at')
        }),
        ('Métadonnées', {
            'fields': ('signature_hash', 'document_hash_at_signing', 'created_at', 'updated_at')
        }),
    )
    
    def status_display(self, obj):
        """Affiche le statut avec une couleur"""
        if obj.is_completed:
            return format_html('<span style="color: green; font-weight: bold;">✓ Signé</span>')
        elif obj.is_rejected:
            return format_html('<span style="color: red; font-weight: bold;">✗ Rejeté</span>')
        else:
            return format_html('<span style="color: orange; font-weight: bold;">⏳ En attente</span>')
    status_display.short_description = 'Statut'