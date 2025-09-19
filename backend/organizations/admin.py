from django.contrib import admin
from .models import Organization, OrganizationMember


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