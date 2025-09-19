from django.contrib import admin
from .models import Organization, OrganizationMember, InvitationCode


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