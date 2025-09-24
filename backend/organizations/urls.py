from django.urls import path
from . import views

urlpatterns = [
    # Création d'organisation
    path('create/', views.create_organization, name='create_organization'),
    
    # Récupération d'organisation
    path('', views.list_all_organizations, name='list_all_organizations'),
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
    path('<int:organization_id>/request-join/', views.request_to_join_organization, name='request_to_join_organization'),
    path('<int:organization_id>/check-membership/', views.check_membership, name='check_membership'),
    path('<int:organization_id>/pending-membership-requests/', views.get_pending_membership_requests, name='get_pending_membership_requests'),
    path('<int:organization_id>/rejected-membership-requests/', views.get_rejected_membership_requests, name='get_rejected_membership_requests'),
    path('<int:organization_id>/all-membership-requests/', views.get_all_membership_requests, name='get_all_membership_requests'),
    path('membership-requests/<int:request_id>/approve/', views.approve_membership_request, name='approve_membership_request'),
    path('membership-requests/<int:request_id>/reject/', views.reject_membership_request, name='reject_membership_request'),
    path('membership-requests/<int:request_id>/reapprove/', views.reapprove_membership_request, name='reapprove_membership_request'),
    path('membership-request/', views.create_membership_request, name='create_membership_request'),
    
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
