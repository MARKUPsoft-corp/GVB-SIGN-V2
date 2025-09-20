from django.urls import path
from . import views

urlpatterns = [
    # Création d'organisation
    path('create/', views.create_organization, name='create_organization'),
    
    # Récupération d'organisation
    path('my-organization/', views.get_user_organization, name='get_user_organization'),
    path('user-organizations/', views.get_user_organizations, name='get_user_organizations'),
    path('<int:organization_id>/leave/', views.leave_organization, name='leave_organization'),
    path('list/', views.list_organizations, name='list_organizations'),
    
    # Gestion d'organisation
    path('<int:organization_id>/', views.get_organization, name='get_organization'),
    path('<int:organization_id>/update/', views.update_organization, name='update_organization'),
    path('<int:organization_id>/delete/', views.delete_organization, name='delete_organization'),
    path('<int:organization_id>/members/', views.get_organization_members, name='get_organization_members'),
    
    # Rejoindre une organisation (utilise maintenant validate_invitation_code)
    path('join/', views.validate_invitation_code, name='join_organization'),
    
    # Codes d'invitation
    path('invitations/create/', views.create_invitation_code, name='create_invitation_code'),
    path('invitations/validate/', views.validate_invitation_code, name='validate_invitation_code'),
    path('invitations/list/', views.list_invitation_codes, name='list_invitation_codes'),
    path('invitations/<int:code_id>/deactivate/', views.deactivate_invitation_code, name='deactivate_invitation_code'),
    path('invitations/<int:code_id>/reactivate/', views.reactivate_invitation_code, name='reactivate_invitation_code'),
    path('invitations/<int:code_id>/delete/', views.delete_invitation_code, name='delete_invitation_code'),
    
    # Certificats d'organisation
    path('<int:organization_id>/certificates/', views.get_organization_certificates, name='get_organization_certificates'),
    path('<int:organization_id>/certificates/create/', views.create_organization_certificate, name='create_organization_certificate'),
    path('<int:organization_id>/certificates/<int:certificate_id>/delete/', views.delete_organization_certificate, name='delete_organization_certificate'),
]
