from django.urls import path
from . import views

urlpatterns = [
    # Création d'organisation
    path('create/', views.create_organization, name='create_organization'),
    
    # Récupération d'organisation
    path('my-organization/', views.get_user_organization, name='get_user_organization'),
    path('user-organizations/', views.get_user_organizations, name='get_user_organizations'),
    path('list/', views.list_organizations, name='list_organizations'),
    
    # Gestion d'organisation
    path('<int:organization_id>/', views.update_organization, name='update_organization'),
    path('<int:organization_id>/delete/', views.delete_organization, name='delete_organization'),
    path('<int:organization_id>/members/', views.get_organization_members, name='get_organization_members'),
    
    # Rejoindre une organisation (utilise maintenant validate_invitation_code)
    path('join/', views.validate_invitation_code, name='join_organization'),
    
    # Codes d'invitation
    path('invitations/create/', views.create_invitation_code, name='create_invitation_code'),
    path('invitations/validate/', views.validate_invitation_code, name='validate_invitation_code'),
    path('invitations/list/', views.list_invitation_codes, name='list_invitation_codes'),
]
