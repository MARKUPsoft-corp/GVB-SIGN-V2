from django.contrib import admin
from .models import Organization, OrganizationMember, InvitationCode, OrganizationCertificate, DemandeAdhesion


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization_type', 'email', 'created_by', 'created_at', 'is_active']
    list_filter = ['organization_type', 'is_active', 'created_at']
    search_fields = ['name', 'email', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'description', 'organization_type', 'sector')
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'address', 'website')
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_active')
        }),
    )


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'joined_at', 'invited_by']
    list_filter = ['role', 'joined_at', 'organization']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'organization__name']
    readonly_fields = ['joined_at']
    fieldsets = (
        ('Membre', {
            'fields': ('user', 'organization', 'role')
        }),
        ('Invitation', {
            'fields': ('invited_by', 'joined_at')
        }),
    )


@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'organization', 'role', 'created_by', 'created_at', 'expires_at', 'is_used', 'is_active']
    list_filter = ['role', 'is_used', 'is_active', 'created_at', 'expires_at', 'organization']
    search_fields = ['code', 'organization__name', 'created_by__first_name', 'created_by__last_name', 'used_by__first_name', 'used_by__last_name']
    readonly_fields = ['code', 'created_at', 'expires_at', 'used_at', 'is_expired', 'is_valid']
    fieldsets = (
        ('Code d\'invitation', {
            'fields': ('code', 'organization', 'role')
        }),
        ('Créateur', {
            'fields': ('created_by', 'created_at')
        }),
        ('Utilisation', {
            'fields': ('used_by', 'used_at', 'is_used')
        }),
        ('Statut', {
            'fields': ('is_active', 'expires_at', 'is_expired', 'is_valid')
        }),
    )
    
    def get_queryset(self, request):
        """Optimiser les requêtes avec select_related"""
        return super().get_queryset(request).select_related(
            'organization', 'created_by', 'used_by'
        )


@admin.register(OrganizationCertificate)
class OrganizationCertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'subject_common_name', 'subject_organization', 'imported_by', 'imported_at', 'is_valid', 'is_active']
    list_filter = ['is_valid', 'is_active', 'imported_at', 'organization', 'signature_algorithm']
    search_fields = ['name', 'subject_common_name', 'subject_organization', 'organization__name', 'imported_by__first_name', 'imported_by__last_name']
    readonly_fields = ['fingerprint', 'serial_number', 'imported_at', 'is_expired', 'days_until_expiry']
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'organization', 'imported_by', 'imported_at', 'is_active')
        }),
        ('Sujet du certificat', {
            'fields': ('subject_common_name', 'subject_organization', 'subject_organizational_unit', 'subject_country', 'subject_email')
        }),
        ('Émetteur du certificat', {
            'fields': ('issuer_common_name', 'issuer_organization', 'issuer_country')
        }),
        ('Détails techniques', {
            'fields': ('serial_number', 'fingerprint', 'signature_algorithm', 'key_usage')
        }),
        ('Validité', {
            'fields': ('not_before', 'not_after', 'is_valid', 'is_expired', 'days_until_expiry')
        }),
        ('Clés et certificat', {
            'fields': ('private_key_pem', 'public_key_pem', 'certificate_pem'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiser les requêtes avec select_related"""
        return super().get_queryset(request).select_related(
            'organization', 'imported_by'
        )


@admin.register(DemandeAdhesion)
class DemandeAdhesionAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'requested_role', 'status', 'created_at', 'processed_at']
    list_filter = ['status', 'requested_role', 'organization', 'created_at', 'processed_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'organization__name']
    readonly_fields = ['created_at', 'updated_at', 'invitation_code']
    
    fieldsets = (
        ('Demande', {
            'fields': ('user', 'organization', 'requested_role', 'message')
        }),
        ('Code d\'invitation', {
            'fields': ('invitation_code',),
            'classes': ('collapse',)
        }),
        ('Statut', {
            'fields': ('status', 'processed_by', 'processed_at', 'response_message')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        """Action pour approuver les demandes sélectionnées"""
        count = 0
        for demande in queryset.filter(status='pending'):
            try:
                demande.approve(request.user, "Demande approuvée par l'administrateur")
                count += 1
            except Exception as e:
                self.message_user(request, f"Erreur lors de l'approbation de {demande}: {str(e)}", level='ERROR')
        
        self.message_user(request, f"{count} demande(s) approuvée(s) avec succès.")
    approve_requests.short_description = "Approuver les demandes sélectionnées"
    
    def reject_requests(self, request, queryset):
        """Action pour rejeter les demandes sélectionnées"""
        count = 0
        for demande in queryset.filter(status='pending'):
            try:
                demande.reject(request.user, "Demande rejetée par l'administrateur")
                count += 1
            except Exception as e:
                self.message_user(request, f"Erreur lors du rejet de {demande}: {str(e)}", level='ERROR')
        
        self.message_user(request, f"{count} demande(s) rejetée(s) avec succès.")
    reject_requests.short_description = "Rejeter les demandes sélectionnées"