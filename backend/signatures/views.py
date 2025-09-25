from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from organizations.models import Organization, OrganizationMember
from .models import DocumentPreparation, DocumentSignatureStep, DocumentSignature
from .serializers import (
    DocumentPreparationSerializer, 
    DocumentSignatureStepSerializer,
    DocumentPreparationCreateSerializer
)

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_document_preparation(request):
    """
    Crée une nouvelle préparation de document
    """
    try:
        # Récupérer l'organisation depuis les données de la requête ou le localStorage
        organization_data = request.data.get('organization')
        if not organization_data:
            return Response({
                'success': False,
                'error': 'Organisation non fournie'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Ajouter le contexte nécessaire
        context = {
            'request': request,
            'organization': organization_data
        }
        
        serializer = DocumentPreparationCreateSerializer(data=request.data, context=context)
        
        if serializer.is_valid():
            document_preparation = serializer.save()
            
            # Sérialiser la réponse
            response_serializer = DocumentPreparationSerializer(document_preparation)
            
            return Response({
                'success': True,
                'message': 'Document préparé avec succès',
                'document_preparation': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document_preparations(request):
    """
    Récupère les préparations de documents de l'utilisateur
    """
    try:
        # Récupérer les préparations où l'utilisateur est soit le préparateur soit le signataire actuel
        preparations = DocumentPreparation.objects.filter(
            models.Q(prepared_by=request.user) | models.Q(current_signer=request.user)
        ).select_related('organization', 'prepared_by', 'current_signer').order_by('-created_at')
        
        serializer = DocumentPreparationSerializer(preparations, many=True)
        
        return Response({
            'success': True,
            'preparations': serializer.data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document_preparation(request, preparation_id):
    """
    Récupère une préparation de document spécifique
    """
    try:
        preparation = get_object_or_404(
            DocumentPreparation,
            id=preparation_id,
            organization__organizationmember__user=request.user
        )
        
        serializer = DocumentPreparationSerializer(preparation)
        
        # Récupérer aussi les étapes de signature
        steps = DocumentSignatureStep.objects.filter(
            document_preparation=preparation
        ).order_by('step_order')
        
        steps_serializer = DocumentSignatureStepSerializer(steps, many=True)
        
        return Response({
            'success': True,
            'preparation': serializer.data,
            'signature_steps': steps_serializer.data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def advance_workflow(request, preparation_id):
    """
    Fait avancer le workflow d'une préparation (pour les signatures)
    """
    try:
        preparation = get_object_or_404(
            DocumentPreparation,
            id=preparation_id,
            current_signer=request.user
        )
        
        # Vérifier que l'utilisateur peut signer
        if preparation.status not in ['prepared', 'pending_signature', 'in_progress']:
            return Response({
                'success': False,
                'error': 'Ce document ne peut plus être signé'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Récupérer les données de signature
        signature_data = request.data.get('signature_data', {})
        
        # Trouver l'étape actuelle
        current_step = DocumentSignatureStep.objects.get(
            document_preparation=preparation,
            step_order=preparation.current_step + 1,
            signer=request.user
        )
        
        # Marquer l'étape comme complétée
        current_step.signature_image = signature_data.get('signature_image', '')
        current_step.signature_position = signature_data.get('signature_position', {})
        current_step.digital_signature = signature_data.get('digital_signature', '')
        current_step.public_key = signature_data.get('public_key', '')
        current_step.signature_hash = signature_data.get('signature_hash', '')
        current_step.document_hash_at_signing = signature_data.get('document_hash', '')
        current_step.is_completed = True
        current_step.signed_at = timezone.now()
        current_step.save()
        
        # Faire avancer le workflow
        preparation.advance_workflow()
        
        # Mettre à jour le document actuel si fourni
        if 'signed_document_data' in request.data:
            from django.core.files.base import ContentFile
            import base64
            
            signed_pdf_data = base64.b64decode(request.data['signed_document_data'])
            signed_file = ContentFile(
                signed_pdf_data, 
                name=f"{preparation.document_id}_step_{current_step.step_order}_{preparation.original_filename}"
            )
            preparation.current_document = signed_file
            preparation.save()
        
        # Si le workflow est complété, créer l'entrée finale dans DocumentSignature
        if preparation.is_completed:
            self._create_final_document_signature(preparation)
        
        serializer = DocumentPreparationSerializer(preparation)
        
        return Response({
            'success': True,
            'message': 'Signature enregistrée avec succès',
            'preparation': serializer.data
        })
        
    except DocumentSignatureStep.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Étape de signature non trouvée'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
                        'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _create_final_document_signature(preparation):
    """
    Crée l'entrée finale dans DocumentSignature quand le workflow est complété
    """
    from django.utils import timezone
    
    # Récupérer l'historique des signatures
    signature_steps = DocumentSignatureStep.objects.filter(
        document_preparation=preparation,
        is_completed=True
    ).order_by('step_order')
    
    # Construire l'historique du workflow
    workflow_history = []
    for step in signature_steps:
        workflow_history.append({
            'step_order': step.step_order,
            'signer_name': step.signer_name,
            'signer_role': step.signer_role,
            'signer_email': step.signer_email,
            'signed_at': step.signed_at.isoformat() if step.signed_at else None,
            'signature_hash': step.signature_hash
        })
    
    # Créer l'entrée DocumentSignature finale
    final_signature = DocumentSignature.objects.create(
        document_id=preparation.document_id,
        document_preparation=preparation,
        organization=preparation.organization,
        user=preparation.prepared_by,  # Le secrétaire qui a initié
        signer_full_name=f"Workflow {preparation.organization.name}",
        original_document=preparation.original_document,
        signed_document=preparation.current_document,
        original_filename=preparation.original_filename,
        document_hash=preparation.elements_configuration.get('document_hash', ''),
        public_key='',  # Pas de clé unique pour un workflow
        signature='WORKFLOW_COMPLETED',
        signature_timestamp=timezone.now(),
        file_size_original=preparation.file_size_original,
        file_size_signed=preparation.current_document.size if preparation.current_document else 0,
        execution_time=0.0,
        workflow_history=workflow_history,
        is_workflow_document=True
    )
    
    # Copier le document final
    if preparation.current_document:
        preparation.final_document = preparation.current_document
        preparation.save()
    
    return final_signature


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pending_signatures(request):
    """
    Récupère les documents en attente de signature pour l'utilisateur
    """
    try:
        pending_preparations = DocumentPreparation.objects.filter(
            current_signer=request.user,
            status__in=['prepared', 'pending_signature', 'in_progress']
        ).select_related('organization', 'prepared_by').order_by('-created_at')
        
        serializer = DocumentPreparationSerializer(pending_preparations, many=True)
        
        return Response({
            'success': True,
            'pending_documents': serializer.data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)