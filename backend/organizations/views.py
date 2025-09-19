from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Organization, OrganizationMember
from .serializers import (
    OrganizationSerializer, 
    OrganizationCreateSerializer, 
    OrganizationListSerializer,
    OrganizationMemberSerializer
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
    if not request.user.organization:
        return Response({
            'success': False,
            'message': 'Vous n\'appartenez à aucune organisation'
        }, status=status.HTTP_404_NOT_FOUND)
    
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
def update_organization(request, organization_id):
    """
    Mettre à jour une organisation
    """
    organization = get_object_or_404(Organization, id=organization_id)
    
    # Vérifier que l'utilisateur est administrateur de cette organisation
    if request.user.organization != organization or request.user.role != 'admin':
        return Response({
            'success': False,
            'message': 'Seuls les administrateurs peuvent modifier l\'organisation'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = OrganizationCreateSerializer(organization, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        
        response_serializer = OrganizationSerializer(organization, context={'request': request})
        
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
def delete_organization(request, organization_id):
    """
    Supprimer une organisation
    """
    organization = get_object_or_404(Organization, id=organization_id)
    
    # Vérifier que l'utilisateur est administrateur de cette organisation
    if request.user.organization != organization or request.user.role != 'admin':
        return Response({
            'success': False,
            'message': 'Seuls les administrateurs peuvent supprimer l\'organisation'
        }, status=status.HTTP_403_FORBIDDEN)
    
    organization.delete()
    
    return Response({
        'success': True,
        'message': 'Organisation supprimée avec succès !'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def join_organization(request):
    """
    Rejoindre une organisation avec un code d'invitation
    """
    invite_code = request.data.get('invite_code')
    
    if not invite_code:
        return Response({
            'success': False,
            'message': 'Code d\'invitation requis'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Pour l'instant, on simule la logique d'invitation
    # Plus tard, on implémentera un système de codes d'invitation
    
    return Response({
        'success': False,
        'message': 'Fonctionnalité de rejoindre une organisation en cours de développement'
    }, status=status.HTTP_501_NOT_IMPLEMENTED)