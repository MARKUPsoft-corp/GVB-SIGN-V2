from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Organization, OrganizationMember, InvitationCode, OrganizationCertificate
from .serializers import (
    OrganizationSerializer, 
    OrganizationCreateSerializer, 
    OrganizationListSerializer,
    OrganizationMemberSerializer,
    InvitationCodeSerializer,
    InvitationCodeCreateSerializer,
    InvitationCodeValidateSerializer,
    OrganizationCertificateSerializer,
    OrganizationCertificateCreateSerializer
)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def create_organization(request):
    """
    Créer une nouvelle organisation
    """
    # Désactiver explicitement la vérification CSRF
    request.csrf_processing_done = True
    
    print(f"🔍 Création d'organisation - Utilisateur: {request.user}")
    print(f"🔍 Utilisateur authentifié: {request.user.is_authenticated}")
    print(f"🔍 Données reçues: {request.data}")
    print(f"🔍 Méthode: {request.method}")
    print(f"🔍 Headers: {dict(request.headers)}")
    
    # Vérifier que l'utilisateur est authentifié
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': 'Utilisateur non authentifié'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = OrganizationSerializer(data=request.data, context={'request': request})
    
    print(f"🔍 Sérialiseur valide: {serializer.is_valid()}")
    if not serializer.is_valid():
        print(f"🔍 Erreurs de validation: {serializer.errors}")
    
    if serializer.is_valid():
        try:
            print(f"🔍 Avant création - Utilisateur: {request.user}")
            print(f"🔍 Avant création - ID utilisateur: {request.user.id}")
            
            # Créer l'organisation (le sérialiseur gère déjà tout)
            organization = serializer.save()
            
            print(f"🔍 Organisation créée avec succès: {organization.id}")
            
            # Retourner les détails de l'organisation créée
            response_serializer = OrganizationSerializer(organization, context={'request': request})
            
            return Response({
                'success': True,
                'message': 'Organisation créée avec succès !',
                'organization': response_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"🔍 Erreur lors de la création: {str(e)}")
            import traceback
            print(f"🔍 Traceback: {traceback.format_exc()}")
            return Response({
                'success': False,
                'message': f'Erreur lors de la création de l\'organisation: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'success': False,
        'message': 'Erreur lors de la création de l\'organisation',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_organization(request):
    """
    Récupérer l'organisation de l'utilisateur connecté
    """
    print(f"🔍 Récupération organisation - Utilisateur: {request.user}")
    print(f"🔍 Organisation de l'utilisateur: {request.user.organization}")
    print(f"🔍 ID organisation: {request.user.organization.id if request.user.organization else 'None'}")
    
    if not request.user.organization:
        print(f"🔍 Aucune organisation trouvée pour l'utilisateur")
        return Response({
            'success': False,
            'message': 'Vous n\'appartenez à aucune organisation'
        }, status=status.HTTP_404_NOT_FOUND)
    
    print(f"🔍 Organisation trouvée: {request.user.organization.name}")
    serializer = OrganizationSerializer(request.user.organization, context={'request': request})
    
    # Ajouter le rôle de l'utilisateur dans l'organisation
    organization_data = serializer.data.copy()
    organization_data['role'] = request.user.role
    organization_data['role_display'] = request.user.get_role_display()
    
    return Response({
        'success': True,
        'organization': organization_data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_organizations(request):
    """
    Lister toutes les organisations (pour les superusers ou admins)
    """
    if not request.user.is_superuser:
        return Response({
            'success': False,
            'message': 'Accès non autorisé'
        }, status=status.HTTP_403_FORBIDDEN)
    
    organizations = Organization.objects.all()
    serializer = OrganizationListSerializer(organizations, many=True)
    
    return Response({
        'success': True,
        'organizations': serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_organization(request, organization_id):
    """
    Récupérer une organisation spécifique
    """
    try:
        organization = get_object_or_404(Organization, id=organization_id)
        
        # Vérifier que l'utilisateur appartient à cette organisation
        user_membership = OrganizationMember.objects.filter(
            user=request.user, 
            organization=organization
        ).first()
        
        if not user_membership:
            return Response({
                'success': False,
                'message': 'Accès non autorisé à cette organisation'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Sérialiser l'organisation avec toutes les données
        serializer = OrganizationSerializer(organization, context={'request': request})
        
        return Response({
            'success': True,
            'organization': serializer.data
        })
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de l'organisation: {str(e)}")
        return Response({
            'success': False,
            'message': 'Erreur lors de la récupération de l\'organisation'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_organizations(request):
    """
    Récupérer toutes les organisations auxquelles appartient l'utilisateur
    """
    try:
        # Récupérer toutes les adhésions de l'utilisateur
        memberships = OrganizationMember.objects.filter(user=request.user).select_related('organization')
        
        organizations_data = []
        for membership in memberships:
            org_data = {
                'id': membership.organization.id,
                'name': membership.organization.name,
                'description': membership.organization.description,
                'email': membership.organization.email,
                'phone': membership.organization.phone,
                'address': membership.organization.address,
                'website': membership.organization.website,
                'organization_type': membership.organization.organization_type,
                'sector': membership.organization.sector,
                'is_active': membership.organization.is_active,
                'member_count': membership.organization.member_count,
                'role': membership.role,
                'role_display': membership.get_role_display(),
                'joined_at': membership.joined_at,
                'status': 'active' if membership.organization.is_active else 'inactive'
            }
            organizations_data.append(org_data)
        
        return Response({
            'success': True,
            'organizations': organizations_data
        })
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des organisations: {str(e)}")
        return Response({
            'success': False,
            'message': 'Erreur lors de la récupération des organisations'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_organization_members(request, organization_id):
    """
    Récupérer les membres d'une organisation
    """
    organization = get_object_or_404(Organization, id=organization_id)
    
    # Vérifier que l'utilisateur appartient à cette organisation via OrganizationMember
    user_membership = OrganizationMember.objects.filter(
        user=request.user, 
        organization=organization
    ).first()
    
    if not user_membership:
        return Response({
            'success': False,
            'message': 'Accès non autorisé à cette organisation'
        }, status=status.HTTP_403_FORBIDDEN)
    
    members = OrganizationMember.objects.filter(organization=organization)
    serializer = OrganizationMemberSerializer(members, many=True)
    
    return Response({
        'success': True,
        'members': serializer.data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def leave_organization(request, organization_id):
    """
    Quitter une organisation
    """
    # Désactiver explicitement la vérification CSRF
    request.csrf_processing_done = True
    
    try:
        print(f"🔍 Tentative de sortie - Utilisateur: {request.user.email}")
        print(f"🔍 ID organisation: {organization_id}")
        
        organization = get_object_or_404(Organization, id=organization_id)
        print(f"🔍 Organisation trouvée: {organization.name}")
        
        # Vérifier que l'utilisateur appartient à cette organisation
        user_membership = OrganizationMember.objects.filter(
            user=request.user, 
            organization=organization
        ).first()
        
        print(f"🔍 Adhésion trouvée: {user_membership}")
        
        if not user_membership:
            # Vérifier si l'utilisateur est l'admin de l'organisation (ancien système)
            if hasattr(request.user, 'organization') and request.user.organization == organization:
                print(f"🔍 Utilisateur admin de l'organisation (ancien système)")
                # Créer un enregistrement OrganizationMember pour l'admin
                user_membership = OrganizationMember.objects.create(
                    user=request.user,
                    organization=organization,
                    role='admin',
                    joined_at=timezone.now()
                )
                print(f"✅ Enregistrement OrganizationMember créé pour l'admin")
            else:
                print(f"❌ Utilisateur {request.user.email} n'appartient pas à l'organisation {organization.name}")
                return Response({
                    'success': False,
                    'message': 'Vous n\'appartenez pas à cette organisation'
                }, status=status.HTTP_403_FORBIDDEN)
        
        # Supprimer l'adhésion de l'utilisateur
        # Le signal post_delete s'occupera automatiquement de réactiver les codes d'invitation
        user_membership.delete()
        
        print(f"✅ Utilisateur {request.user.email} a quitté l'organisation {organization.name}")
        
        return Response({
            'success': True,
            'message': f'Vous avez quitté l\'organisation {organization.name} avec succès'
        })
        
    except Exception as e:
        print(f"❌ Erreur lors de la sortie de l'organisation: {str(e)}")
        return Response({
            'success': False,
            'message': 'Erreur lors de la sortie de l\'organisation'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def update_organization(request, organization_id):
    """
    Mettre à jour une organisation
    """
    # Désactiver explicitement la vérification CSRF
    request.csrf_processing_done = True
    
    print(f"🔍 Mise à jour organisation - Utilisateur: {request.user}")
    print(f"🔍 ID organisation: {organization_id}")
    print(f"🔍 Données reçues: {request.data}")
    
    organization = get_object_or_404(Organization, id=organization_id)
    
    # Vérifier que l'utilisateur est administrateur de cette organisation via OrganizationMember
    user_membership = OrganizationMember.objects.filter(
        user=request.user, 
        organization=organization,
        role='admin'
    ).first()
    
    if not user_membership:
        # Vérifier si l'utilisateur appartient à l'organisation avec un autre rôle
        other_membership = OrganizationMember.objects.filter(
            user=request.user, 
            organization=organization
        ).first()
        
        user_role = other_membership.role if other_membership else 'Aucun'
        print(f"🔍 ERREUR: Utilisateur non autorisé - Organisation: {organization.name}, Rôle de l'utilisateur: {user_role}")
        return Response({
            'success': False,
            'message': f'Seuls les administrateurs peuvent modifier l\'organisation. Votre rôle: {user_role}'
        }, status=status.HTTP_403_FORBIDDEN)
    
    print(f"🔍 Utilisateur autorisé - Utilisation d'OrganizationSerializer")
    serializer = OrganizationSerializer(organization, data=request.data, partial=True, context={'request': request})
    
    print(f"🔍 Sérialiseur valide: {serializer.is_valid()}")
    if not serializer.is_valid():
        print(f"🔍 Erreurs de validation: {serializer.errors}")
    
    if serializer.is_valid():
        serializer.save()
        
        response_serializer = OrganizationSerializer(organization, context={'request': request})
        
        print(f"🔍 Organisation mise à jour avec succès")
        return Response({
            'success': True,
            'message': 'Organisation mise à jour avec succès !',
            'organization': response_serializer.data
        })
    
    return Response({
        'success': False,
        'message': 'Erreur lors de la mise à jour de l\'organisation',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def delete_organization(request, organization_id):
    """
    Supprimer une organisation
    """
    # Désactiver explicitement la vérification CSRF
    request.csrf_processing_done = True
    
    print(f"🔍 Suppression organisation - Utilisateur: {request.user}")
    print(f"🔍 ID organisation: {organization_id}")
    print(f"🔍 Données reçues: {request.data}")
    
    organization = get_object_or_404(Organization, id=organization_id)
    
    # Vérifier que l'utilisateur est administrateur de cette organisation
    if request.user.organization != organization or request.user.role != 'admin':
        print(f"🔍 ERREUR: Utilisateur non autorisé - Organisation: {request.user.organization}, Rôle: {request.user.role}")
        return Response({
            'success': False,
            'message': 'Seuls les administrateurs peuvent supprimer l\'organisation'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Vérifier le mot de passe
    password = request.data.get('password')
    if not password:
        print(f"🔍 ERREUR: Aucun mot de passe fourni")
        return Response({
            'success': False,
            'message': 'Mot de passe requis pour supprimer l\'organisation'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Vérifier que le mot de passe est correct
    if not request.user.check_password(password):
        print(f"🔍 ERREUR: Mot de passe incorrect")
        return Response({
            'success': False,
            'message': 'Mot de passe incorrect'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    print(f"🔍 Mot de passe correct, suppression de l'organisation")
    
    # Supprimer l'organisation
    organization.delete()
    
    print(f"🔍 Organisation supprimée avec succès")
    
    return Response({
        'success': True,
        'message': 'Organisation supprimée avec succès !'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def create_invitation_code(request):
    """
    Créer un code d'invitation pour une organisation
    """
    print(f"🔍 === CRÉATION D'UN CODE D'INVITATION ===")
    print(f"🔍 Utilisateur: {request.user}")
    print(f"🔍 Données reçues: {request.data}")
    
    serializer = InvitationCodeCreateSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        try:
            invitation_code = serializer.save()
            print(f"🔍 Code d'invitation créé: {invitation_code.code}")
            
            # Sérialiser la réponse
            response_serializer = InvitationCodeSerializer(invitation_code)
            
            return Response({
                'success': True,
                'message': 'Code d\'invitation généré avec succès !',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"🔍 Erreur lors de la création: {str(e)}")
            return Response({
                'success': False,
                'message': f'Erreur lors de la création du code d\'invitation: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print(f"🔍 Erreurs de validation: {serializer.errors}")
        return Response({
            'success': False,
            'message': 'Données invalides',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def validate_invitation_code(request):
    """
    Valider un code d'invitation et rejoindre l'organisation
    """
    print(f"🔍 === VALIDATION D'UN CODE D'INVITATION ===")
    print(f"🔍 Utilisateur: {request.user}")
    print(f"🔍 Code reçu: {request.data.get('code')}")
    
    serializer = InvitationCodeValidateSerializer(data=request.data)
    
    if serializer.is_valid():
        code = serializer.validated_data['code']
        
        try:
            # Récupérer le code d'invitation
            invitation_code = InvitationCode.objects.get(code=code)
            print(f"🔍 Code trouvé: {invitation_code}")
            print(f"🔍 Organisation: {invitation_code.organization.name}")
            print(f"🔍 Rôle: {invitation_code.role}")
            
            # Vérifier si l'utilisateur n'est pas déjà membre de cette organisation
            existing_member = OrganizationMember.objects.filter(
                organization=invitation_code.organization,
                user=request.user
            ).first()
            
            if existing_member:
                # L'utilisateur est déjà membre de cette organisation
                role_display = existing_member.get_role_display()
                return Response({
                    'success': True,
                    'already_member': True,
                    'message': f'Vous appartenez déjà à l\'organisation {invitation_code.organization.name}',
                    'organization': {
                        'id': invitation_code.organization.id,
                        'name': invitation_code.organization.name,
                        'role': existing_member.role
                    },
                    'role_display': role_display
                }, status=status.HTTP_200_OK)
            
            # Vérifier si l'utilisateur essaie d'utiliser un code qu'il a lui-même créé
            if invitation_code.created_by == request.user:
                return Response({
                    'success': True,
                    'already_member': True,
                    'message': f'Vous êtes déjà administrateur de l\'organisation {invitation_code.organization.name}',
                    'organization': {
                        'id': invitation_code.organization.id,
                        'name': invitation_code.organization.name,
                        'role': 'admin'
                    },
                    'role_display': 'Administrateur'
                }, status=status.HTTP_200_OK)
            
            # Utiliser le code d'invitation
            invitation_code.use_code(request.user)
            print(f"🔍 Code utilisé avec succès par {request.user.full_name}")
            
            # Mettre à jour l'utilisateur pour qu'il appartienne à cette organisation
            request.user.organization = invitation_code.organization
            request.user.role = invitation_code.role
            request.user.save()
            
            return Response({
                'success': True,
                'message': f'Vous avez rejoint l\'organisation {invitation_code.organization.name} avec succès !',
                'organization': {
                    'id': invitation_code.organization.id,
                    'name': invitation_code.organization.name,
                    'role': invitation_code.role
                }
            }, status=status.HTTP_200_OK)
            
        except InvitationCode.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Code d\'invitation invalide.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"🔍 Erreur lors de la validation: {str(e)}")
            return Response({
                'success': False,
                'message': f'Erreur lors de la validation du code: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print(f"🔍 Erreurs de validation: {serializer.errors}")
        return Response({
            'success': False,
            'message': 'Code d\'invitation invalide',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_invitation_codes(request):
    """
    Lister les codes d'invitation d'une organisation
    """
    try:
        organization_id = request.GET.get('organization_id')
        
        if not organization_id:
            return Response({
                'success': False,
                'message': 'ID de l\'organisation requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier que l'utilisateur appartient à cette organisation
        user_membership = OrganizationMember.objects.filter(
            user=request.user, 
            organization_id=organization_id
        ).first()
        
        if not user_membership:
            return Response({
                'success': False,
                'message': 'Accès non autorisé à cette organisation'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Récupérer les codes d'invitation de l'organisation
        invitation_codes = InvitationCode.objects.filter(
            organization_id=organization_id
        ).order_by('-created_at')
        
        serializer = InvitationCodeSerializer(invitation_codes, many=True)
        
        return Response({
            'success': True,
            'invitation_codes': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des codes d'invitation: {str(e)}")
        return Response({
            'success': False,
            'message': f'Erreur lors de la récupération des codes: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def deactivate_invitation_code(request, code_id):
    """
    Désactiver un code d'invitation
    """
    try:
        invitation_code = get_object_or_404(InvitationCode, id=code_id)
        
        # Vérifier que l'utilisateur appartient à cette organisation
        user_membership = OrganizationMember.objects.filter(
            user=request.user, 
            organization=invitation_code.organization
        ).first()
        
        if not user_membership:
            return Response({
                'success': False,
                'message': 'Accès non autorisé à cette organisation'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Désactiver le code
        invitation_code.is_active = False
        invitation_code.save()
        
        print(f"✅ Code d'invitation {invitation_code.code} désactivé")
        
        return Response({
            'success': True,
            'message': 'Code d\'invitation désactivé avec succès'
        })
        
    except Exception as e:
        print(f"❌ Erreur lors de la désactivation du code: {str(e)}")
        return Response({
            'success': False,
            'message': f'Erreur lors de la désactivation du code: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reactivate_invitation_code(request, code_id):
    """
    Réactiver un code d'invitation
    """
    try:
        invitation_code = get_object_or_404(InvitationCode, id=code_id)
        
        # Vérifier que l'utilisateur appartient à cette organisation
        user_membership = OrganizationMember.objects.filter(
            user=request.user, 
            organization=invitation_code.organization
        ).first()
        
        if not user_membership:
            return Response({
                'success': False,
                'message': 'Accès non autorisé à cette organisation'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Réactiver le code
        invitation_code.is_active = True
        invitation_code.save()
        
        print(f"✅ Code d'invitation {invitation_code.code} réactivé")
        
        return Response({
            'success': True,
            'message': 'Code d\'invitation réactivé avec succès'
        })
        
    except Exception as e:
        print(f"❌ Erreur lors de la réactivation du code: {str(e)}")
        return Response({
            'success': False,
            'message': f'Erreur lors de la réactivation du code: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_invitation_code(request, code_id):
    """
    Supprimer définitivement un code d'invitation
    """
    try:
        invitation_code = get_object_or_404(InvitationCode, id=code_id)
        
        # Vérifier que l'utilisateur appartient à cette organisation
        user_membership = OrganizationMember.objects.filter(
            user=request.user, 
            organization=invitation_code.organization
        ).first()
        
        if not user_membership:
            return Response({
                'success': False,
                'message': 'Accès non autorisé à cette organisation'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Supprimer le code
        code_value = invitation_code.code
        invitation_code.delete()
        
        print(f"✅ Code d'invitation {code_value} supprimé définitivement")
        
        return Response({
            'success': True,
            'message': 'Code d\'invitation supprimé avec succès'
        })
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression du code: {str(e)}")
        return Response({
            'success': False,
            'message': f'Erreur lors de la suppression du code: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_organization_certificates(request, organization_id):
    """
    Récupérer les certificats d'une organisation
    """
    try:
        organization = get_object_or_404(Organization, id=organization_id)
        
        # Vérifier que l'utilisateur appartient à cette organisation
        user_membership = OrganizationMember.objects.filter(
            user=request.user, 
            organization=organization
        ).first()
        
        if not user_membership:
            return Response({
                'success': False,
                'message': 'Accès non autorisé à cette organisation'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Récupérer les certificats de l'organisation
        certificates = OrganizationCertificate.objects.filter(
            organization=organization,
            is_active=True
        ).order_by('-imported_at')
        
        serializer = OrganizationCertificateSerializer(certificates, many=True)
        
        return Response({
            'success': True,
            'certificates': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des certificats: {str(e)}")
        return Response({
            'success': False,
            'message': f'Erreur lors de la récupération des certificats: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_organization_certificate(request, organization_id):
    """
    Créer un certificat pour une organisation
    """
    try:
        organization = get_object_or_404(Organization, id=organization_id)
        
        # Vérifier que l'utilisateur appartient à cette organisation
        user_membership = OrganizationMember.objects.filter(
            user=request.user, 
            organization=organization
        ).first()
        
        if not user_membership:
            return Response({
                'success': False,
                'message': 'Accès non autorisé à cette organisation'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Ajouter l'organisation et l'utilisateur aux données
        certificate_data = request.data.copy()
        certificate_data['organization'] = organization.id
        certificate_data['imported_by'] = request.user.id
        
        serializer = OrganizationCertificateCreateSerializer(data=certificate_data)
        
        if serializer.is_valid():
            certificate = serializer.save()
            print(f"✅ Certificat créé: {certificate.name}")
            
            # Retourner le certificat avec toutes les informations
            response_serializer = OrganizationCertificateSerializer(certificate)
            
            return Response({
                'success': True,
                'message': 'Certificat importé avec succès',
                'certificate': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': 'Erreur de validation',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        print(f"❌ Erreur lors de la création du certificat: {str(e)}")
        return Response({
            'success': False,
            'message': f'Erreur lors de la création du certificat: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_organization_certificate(request, organization_id, certificate_id):
    """
    Supprimer un certificat d'organisation
    """
    try:
        organization = get_object_or_404(Organization, id=organization_id)
        
        # Vérifier que l'utilisateur appartient à cette organisation
        user_membership = OrganizationMember.objects.filter(
            user=request.user, 
            organization=organization
        ).first()
        
        if not user_membership:
            return Response({
                'success': False,
                'message': 'Accès non autorisé à cette organisation'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Récupérer le certificat
        certificate = get_object_or_404(OrganizationCertificate, id=certificate_id, organization=organization)
        
        # Supprimer le certificat
        certificate_name = certificate.name
        certificate.delete()
        
        print(f"✅ Certificat {certificate_name} supprimé")
        
        return Response({
            'success': True,
            'message': 'Certificat supprimé avec succès'
        })
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression du certificat: {str(e)}")
        return Response({
            'success': False,
            'message': f'Erreur lors de la suppression du certificat: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)