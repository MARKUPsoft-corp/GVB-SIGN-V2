from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Organization, OrganizationMember, InvitationCode
from .serializers import (
    OrganizationSerializer, 
    OrganizationCreateSerializer, 
    OrganizationListSerializer,
    OrganizationMemberSerializer,
    InvitationCodeSerializer,
    InvitationCodeCreateSerializer,
    InvitationCodeValidateSerializer
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
    
    return Response({
        'success': True,
        'organization': serializer.data
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
def get_organization_members(request, organization_id):
    """
    Récupérer les membres d'une organisation
    """
    organization = get_object_or_404(Organization, id=organization_id)
    
    # Vérifier que l'utilisateur appartient à cette organisation
    if request.user.organization != organization:
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
    
    # Vérifier que l'utilisateur est administrateur de cette organisation
    if request.user.organization != organization or request.user.role != 'admin':
        print(f"🔍 ERREUR: Utilisateur non autorisé - Organisation: {request.user.organization}, Rôle: {request.user.role}")
        return Response({
            'success': False,
            'message': 'Seuls les administrateurs peuvent modifier l\'organisation'
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
            if OrganizationMember.objects.filter(
                organization=invitation_code.organization,
                user=request.user
            ).exists():
                return Response({
                    'success': False,
                    'message': 'Vous êtes déjà membre de cette organisation.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
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
        # Récupérer l'organisation de l'utilisateur
        user_organization = request.user.organization
        if not user_organization:
            return Response({
                'success': False,
                'message': 'Vous n\'appartenez à aucune organisation.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Récupérer les codes d'invitation de l'organisation
        invitation_codes = InvitationCode.objects.filter(
            organization=user_organization
        ).order_by('-created_at')
        
        serializer = InvitationCodeSerializer(invitation_codes, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erreur lors de la récupération des codes: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)