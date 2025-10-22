from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils import timezone
from django.http import FileResponse, Http404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import os
import base64
from django.core.files.base import ContentFile
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
    Récupère les préparations de documents de l'utilisateur pour l'organisation actuelle
    """
    try:
        # Récupérer l'organisation depuis les paramètres de la requête
        organization_id = request.GET.get('organization_id')
        
        if not organization_id:
            return Response({
                'success': False,
                'error': 'ID de l\'organisation requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier que l'utilisateur est membre de cette organisation
        try:
            from organizations.models import OrganizationMember
            membership = OrganizationMember.objects.get(
                user=request.user,
                organization_id=organization_id
            )
        except OrganizationMember.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Vous n\'êtes pas membre de cette organisation'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Récupérer les préparations où l'utilisateur est soit le préparateur soit le signataire actuel
        # ET qui appartiennent à l'organisation spécifiée
        preparations = DocumentPreparation.objects.filter(
            models.Q(prepared_by=request.user) | models.Q(current_signer=request.user),
            organization_id=organization_id
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
            organization__members__user=request.user
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
def save_document_signature(request, preparation_id):
    """
    Enregistre le résultat d'une signature de document
    """
    try:
        # Récupérer la préparation de document
        preparation = get_object_or_404(
            DocumentPreparation,
            id=preparation_id,
            organization__members__user=request.user
        )
        
        # Vérifier que l'utilisateur est le signataire actuel
        if preparation.current_signer != request.user:
            return Response({
                'success': False,
                'error': 'Vous n\'êtes pas autorisé à signer ce document'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Récupérer les données de la requête
        data = request.data
        
        # Validation des données requises
        required_fields = ['document_id', 'document_hash', 'signature', 'public_key', 'signed_document_data', 'file_size_original', 'file_size_signed', 'execution_time']
        for field in required_fields:
            if field not in data:
                return Response({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Décoder le document signé (base64)
        try:
            import base64
            signed_document_data = base64.b64decode(data['signed_document_data'])
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erreur lors du décodage du document signé: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Créer le fichier signé
        from django.core.files.base import ContentFile
        signed_filename = f"{data['document_id']}_signed_{preparation.original_filename}"
        signed_file = ContentFile(signed_document_data, name=signed_filename)
        
        # VÉRIFICATION AUTOMATIQUE DE LA SIGNATURE
        print("🔐 Vérification automatique de la signature avant enregistrement...")
        from .utils import verify_document_signature
        verification_result = verify_document_signature(
            signature_base64=data['signature'],
            public_key_pem=data['public_key'],
            stored_hash=data['document_hash']
        )
        
        if not verification_result['valid']:
            print(f"❌ ATTENTION: Signature invalide détectée!")
            print(f"❌ Message: {verification_result['message']}")
            # On log l'erreur mais on n'empêche pas l'enregistrement pour le moment
            # En production, on pourrait rejeter la signature invalide
        else:
            print(f"✅ Signature vérifiée et valide!")
        
        # Créer l'enregistrement de signature
        signature_record = DocumentSignature.objects.create(
            document_id=data['document_id'],
            document_preparation=preparation,
            user=request.user,
            signer_full_name=request.user.get_full_name(),
            original_document=preparation.original_document,
            signed_document=signed_file,
            original_filename=preparation.original_filename,
            document_hash=data['document_hash'],
            public_key=data['public_key'],
            signature=data['signature'],
            signature_timestamp=data.get('signature_timestamp', timezone.now()),
            # Champs requis supplémentaires
            file_size_original=data['file_size_original'],
            file_size_signed=data['file_size_signed'],
            execution_time=data['execution_time'],
            # Informations sur l'organisation
            organization=preparation.organization,
            workflow_history=preparation.signature_workflow or [],
            is_workflow_document=True
        )
        
        # Mettre à jour la préparation de document
        preparation.current_document = signed_file
        preparation.status = 'in_progress'
        preparation.save()
        
        # Avancer le workflow si ce n'est pas la dernière étape
        from .utils import advance_workflow_step
        workflow_result = advance_workflow_step(preparation)
        
        return Response({
            'success': True,
            'message': 'Signature enregistrée avec succès',
            'signature_id': signature_record.id,
            'workflow_advanced': workflow_result['advanced'],
            'next_signer': workflow_result.get('next_signer'),
            'is_complete': workflow_result.get('is_complete', False)
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement de la signature: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': f'Erreur lors de l\'enregistrement: {str(e)}'
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
            # TODO: Implémenter la création de l'entrée finale si nécessaire
            pass
        
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
@permission_classes([])  # Pas d'authentification requise pour la vérification publique
def verify_signature_by_document_id(request, document_id):
    """
    Vérifie la validité d'une signature de document par son ID (celui du QR code)
    API publique pour vérifier les signatures via QR code
    """
    try:
        print(f"🔐 Vérification de signature pour document ID: {document_id}")
        
        # Récupérer la signature par document_id
        signature_record = get_object_or_404(DocumentSignature, document_id=document_id)
        
        print(f"📄 Document trouvé: {signature_record.original_filename}")
        print(f"👤 Signataire: {signature_record.signer_full_name}")
        print(f"🏢 Organisation: {signature_record.organization.name if signature_record.organization else 'N/A'}")
        
        # Vérifier la signature
        from .utils import verify_signature_record
        verification_result = verify_signature_record(signature_record)
        
        # Préparer les données de réponse
        response_data = {
            'success': True,
            'document_info': {
                'document_id': signature_record.document_id,
                'filename': signature_record.original_filename,
                'signer_name': signature_record.signer_full_name,
                'signer_email': signature_record.user.email,
                'signature_timestamp': signature_record.signature_timestamp.isoformat(),
                'created_at': signature_record.created_at.isoformat(),
                'file_size_original': signature_record.file_size_original,
                'file_size_signed': signature_record.file_size_signed,
                'execution_time': signature_record.execution_time
            },
            'organization_info': {
                'name': signature_record.organization.name if signature_record.organization else None,
                'id': str(signature_record.organization.id) if signature_record.organization else None
            },
            'verification': verification_result,
            'document_urls': {
                'signed_document_url': signature_record.signed_document.url if signature_record.signed_document else None,
                'original_document_url': signature_record.original_document.url if signature_record.original_document else None
            }
        }
        
        # Ajouter les informations de workflow si disponible
        if signature_record.is_workflow_document and signature_record.workflow_history:
            response_data['workflow_info'] = {
                'is_workflow_document': signature_record.is_workflow_document,
                'workflow_history': signature_record.workflow_history,
                'total_steps': len(signature_record.workflow_history)
            }
        
        print(f"✅ Vérification terminée - Signature valide: {verification_result['valid']}")
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la signature: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': f'Erreur lors de la vérification: {str(e)}',
            'document_id': document_id
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_signed_documents(request):
    """
    Récupère les documents signés pour l'organisation de l'utilisateur
    """
    try:
        # Récupérer l'ID de l'organisation depuis les paramètres
        organization_id = request.GET.get('organization_id')
        
        if not organization_id:
            return Response({
                'success': False,
                'error': 'organization_id est requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier que l'utilisateur appartient à l'organisation
        user_membership = OrganizationMember.objects.filter(
            user=request.user,
            organization_id=organization_id
        ).first()
        
        if not user_membership:
            return Response({
                'success': False,
                'error': 'Accès non autorisé à cette organisation'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Récupérer les documents signés de l'organisation
        signed_documents = DocumentSignature.objects.filter(
            organization_id=organization_id
        ).select_related(
            'user',
            'organization',
            'document_preparation'
        ).order_by('-created_at')
        
        # Sérialiser les documents
        documents_data = []
        for doc in signed_documents:
            documents_data.append({
                'id': str(doc.id),
                'document_id': doc.document_id,
                'original_filename': doc.original_filename,
                'signer_name': doc.signer_full_name,
                'signer_email': doc.user.email,
                'signature_timestamp': doc.signature_timestamp.isoformat(),
                'created_at': doc.created_at.isoformat(),
                'document_hash': doc.document_hash,
                'file_size_original': doc.file_size_original,
                'file_size_signed': doc.file_size_signed,
                'execution_time': doc.execution_time,
                'organization_name': doc.organization.name if doc.organization else None,
                'is_workflow_document': doc.is_workflow_document,
                'workflow_history': doc.workflow_history,
                'original_document_url': doc.original_document.url if doc.original_document else None,
                'signed_document_url': doc.signed_document.url if doc.signed_document else None,
                # Informations sur la préparation si disponible
                'preparation_id': str(doc.document_preparation.id) if doc.document_preparation else None,
                'preparation_status': doc.document_preparation.status if doc.document_preparation else None,
                'preparation_title': doc.document_preparation.document_title if doc.document_preparation else None
            })
        
        return Response({
            'success': True,
            'documents': documents_data,
            'total': len(documents_data)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des documents signés: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': f'Erreur lors de la récupération des documents signés: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


@xframe_options_exempt
@require_http_methods(["GET"])
def serve_pdf_for_preview(request, document_id, file_type):
    """
    Serve un PDF pour l'aperçu dans les iframes sans restrictions X-Frame-Options
    """
    try:
        # Récupérer le document
        document = get_object_or_404(DocumentPreparation, id=document_id)
        
        # Vérifier que l'utilisateur a accès à ce document
        if not request.user.is_authenticated:
            raise Http404("Accès non autorisé")
        
        # Déterminer le chemin du fichier selon le type
        if file_type == 'current':
            # Utiliser la nouvelle logique pour déterminer le document actuel
            if document.status == 'draft':
                # En brouillon, retourner le document original
                if not document.original_document:
                    raise Http404("Document original non trouvé")
                file_path = document.original_document.path
            elif document.status in ['prepared', 'pending_signature', 'in_progress']:
                # En cours de workflow, retourner le document actuel (avec signatures partielles)
                if document.current_document:
                    file_path = document.current_document.path
                elif document.original_document:
                    file_path = document.original_document.path
                else:
                    raise Http404("Document actuel non trouvé")
            elif document.status == 'completed':
                # Workflow terminé, retourner le document final
                if document.final_document:
                    file_path = document.final_document.path
                elif document.current_document:
                    file_path = document.current_document.path
                else:
                    raise Http404("Document final non trouvé")
            else:
                # Par défaut, retourner le document original
                if not document.original_document:
                    raise Http404("Document original non trouvé")
                file_path = document.original_document.path
        elif file_type == 'generated' and document.generated_pdf:
            file_path = document.generated_pdf.path
        else:
            raise Http404("Fichier non trouvé")
        
        # Vérifier que le fichier existe
        if not os.path.exists(file_path):
            raise Http404("Fichier non trouvé sur le serveur")
        
        # Servir le fichier avec les bons headers
        response = FileResponse(
            open(file_path, 'rb'),
            content_type='application/pdf',
            as_attachment=False
        )
        
        # Déterminer si c'est pour l'affichage (inline) ou le téléchargement (attachment)
        is_download = request.GET.get('download', 'false').lower() == 'true'
        
        if is_download:
            # Headers pour le téléchargement
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        else:
            # Headers pour l'affichage dans les iframes
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
            response['X-Frame-Options'] = 'ALLOWALL'  # Permet l'affichage dans toutes les iframes
        
        return response
        
    except Exception as e:
        raise Http404(f"Erreur lors du chargement du fichier: {str(e)}")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_create_signatures(request):
    """
    Crée plusieurs signatures en une seule requête
    """
    try:
        signatures_data = request.data.get('signatures', [])
        
        if not signatures_data:
            return Response({
                'success': False,
                'message': 'Aucune signature fournie',
                'total_processed': 0,
                'total_created': 0,
                'total_errors': 0,
                'created_signatures': [],
                'errors': []
            }, status=status.HTTP_400_BAD_REQUEST)
        
        created_signatures = []
        errors = []
        
        with transaction.atomic():
            for index, signature_data in enumerate(signatures_data):
                try:
                    # Décoder les fichiers base64
                    original_document_data = base64.b64decode(signature_data['original_document_base64'])
                    signed_document_data = base64.b64decode(signature_data['signed_document_base64'])
                    
                    # Créer les fichiers
                    original_filename = signature_data['original_filename']
                    document_id = signature_data['document_id']
                    
                    original_file = ContentFile(
                        original_document_data, 
                        name=f"{document_id}_original_{original_filename}"
                    )
                    signed_file = ContentFile(
                        signed_document_data, 
                        name=f"{document_id}_signed_{original_filename}"
                    )
                    
                    # Créer l'enregistrement de signature
                    signature = DocumentSignature.objects.create(
                        document_id=document_id,
                        user=request.user,
                        signer_full_name=signature_data['signer_full_name'],
                        original_document=original_file,
                        signed_document=signed_file,
                        original_filename=original_filename,
                        document_hash=signature_data['document_hash'],
                        public_key=signature_data['public_key'],
                        signature=signature_data['signature'],
                        signature_timestamp=timezone.now(),
                        file_size_original=signature_data['file_size_original'],
                        file_size_signed=signature_data['file_size_signed'],
                        execution_time=signature_data['execution_time'],
                        organization=request.user.organization if hasattr(request.user, 'organization') else None
                    )
                    
                    created_signatures.append({
                        'index': index,
                        'signature_id': str(signature.id),
                        'document_id': document_id,
                        'status': 'created'
                    })
                    
                except Exception as e:
                    errors.append({
                        'index': index,
                        'document_id': signature_data.get('document_id', 'unknown'),
                        'error': str(e)
                    })
        
        total_processed = len(signatures_data)
        total_created = len(created_signatures)
        total_errors = len(errors)
        
        return Response({
            'success': True,
            'message': f'{total_created} signature(s) créée(s), {total_errors} erreur(s)',
            'total_processed': total_processed,
            'total_created': total_created,
            'total_errors': total_errors,
            'created_signatures': created_signatures,
            'errors': errors
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erreur lors de la création des signatures: {str(e)}',
            'total_processed': 0,
            'total_created': 0,
            'total_errors': 1,
            'created_signatures': [],
            'errors': [{'index': 0, 'document_id': 'unknown', 'error': str(e)}]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)