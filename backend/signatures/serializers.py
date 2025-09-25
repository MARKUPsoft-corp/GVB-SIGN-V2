from rest_framework import serializers
from django.contrib.auth import get_user_model
from organizations.models import Organization, OrganizationMember
from .models import DocumentPreparation, DocumentSignatureStep, DocumentSignature

User = get_user_model()


class DocumentPreparationSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création et la gestion des préparations de documents
    """
    prepared_by_name = serializers.CharField(source='prepared_by.get_full_name', read_only=True)
    current_signer_name = serializers.CharField(source='current_signer.get_full_name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = DocumentPreparation
        fields = [
            'id', 'document_id', 'organization', 'prepared_by', 'current_signer',
            'original_filename', 'document_title', 'document_description',
            'original_document', 'current_document', 'final_document', 'generated_pdf',
            'qr_code_x', 'qr_code_y', 'qr_code_size', 'qr_code_page',
            'signature_x', 'signature_y', 'signature_width', 'signature_height', 'signature_page',
            'elements_configuration', 'secretary_signature_image',
            'signature_workflow', 'current_step', 'total_steps',
            'status', 'created_at', 'updated_at', 'prepared_at', 'completed_at',
            'file_size_original', 'preparation_notes',
            'prepared_by_name', 'current_signer_name', 'organization_name', 'progress_percentage'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'progress_percentage']
    
    def create(self, validated_data):
        """
        Crée une nouvelle préparation de document avec le workflow automatique
        """
        # Récupérer l'organisation et définir le workflow
        organization = validated_data['organization']
        
        # Récupérer les membres de l'organisation avec les rôles de chef
        chiefs = OrganizationMember.objects.filter(
            organization=organization,
            role__in=['chef', 'chef+1', 'chef+2', 'chef+n']
        ).order_by('role')
        
        # Construire le workflow de signature
        workflow = []
        for i, chief in enumerate(chiefs):
            workflow.append({
                'step': i + 1,
                'user_id': chief.user.id,
                'user_name': chief.user.get_full_name(),
                'user_email': chief.user.email,
                'role': chief.role,
                'organization_member_id': chief.id
            })
        
        validated_data['signature_workflow'] = workflow
        validated_data['total_steps'] = len(workflow)
        validated_data['current_step'] = 0  # 0 = préparation
        
        # Définir le premier signataire (chef)
        if workflow:
            try:
                validated_data['current_signer'] = User.objects.get(id=workflow[0]['user_id'])
            except User.DoesNotExist:
                pass
        
        # Créer la préparation
        document_preparation = super().create(validated_data)
        
        # Créer les étapes de signature
        for step_data in workflow:
            DocumentSignatureStep.objects.create(
                document_preparation=document_preparation,
                step_order=step_data['step'],
                signer_id=step_data['user_id'],
                organization_member_id=step_data['organization_member_id'],
                signer_name=step_data['user_name'],
                signer_role=step_data['role'],
                signer_email=step_data['user_email']
            )
        
        return document_preparation


class DocumentSignatureStepSerializer(serializers.ModelSerializer):
    """
    Serializer pour les étapes de signature
    """
    signer_name = serializers.CharField(read_only=True)
    signer_role = serializers.CharField(read_only=True)
    signer_email = serializers.CharField(read_only=True)
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentSignatureStep
        fields = [
            'id', 'step_order', 'signer', 'signer_name', 'signer_role', 'signer_email',
            'signature_image', 'signature_position', 'digital_signature', 'public_key',
            'signed_at', 'signature_hash', 'document_hash_at_signing',
            'is_completed', 'is_rejected', 'rejection_reason',
            'created_at', 'updated_at', 'status_display'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'signer_name', 'signer_role', 'signer_email']
    
    def get_status_display(self, obj):
        """Retourne le statut en format lisible"""
        if obj.is_completed:
            return 'completed'
        elif obj.is_rejected:
            return 'rejected'
        else:
            return 'pending'


class DocumentPreparationCreateSerializer(serializers.Serializer):
    """
    Serializer spécialisé pour la création de préparations de documents depuis le frontend
    """
    # Informations du document
    document_title = serializers.CharField(max_length=255)
    document_description = serializers.CharField(required=False, allow_blank=True)
    original_filename = serializers.CharField(max_length=255)
    
    # Configuration simplifiée des éléments (positions et tailles uniquement)
    elements_configuration = serializers.JSONField(help_text="Configuration avec positions x,y et tailles des éléments")
    signature_image = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text="Image de signature en base64")
    
    # Fichiers (en base64)
    original_document_data = serializers.CharField(help_text="Document PDF original en base64")
    current_document_data = serializers.CharField(required=False, allow_blank=True, help_text="Document PDF actuel en base64")
    final_document_data = serializers.CharField(required=False, allow_blank=True, help_text="PDF généré avec éléments positionnés en base64")
    has_positioned_elements = serializers.BooleanField(required=False, default=False, help_text="Indique si le document a des éléments positionnés")
    
    # Métadonnées
    file_size_original = serializers.IntegerField()
    preparation_notes = serializers.CharField(required=False, allow_blank=True)
    
    def create(self, validated_data):
        """
        Crée une préparation de document avec les données du frontend
        """
        from django.core.files.base import ContentFile
        from django.utils import timezone
        import base64
        import uuid
        
        # Récupérer l'utilisateur et l'organisation depuis le contexte
        user = self.context['request'].user
        organization_data = self.context.get('organization')
        
        if not organization_data:
            raise serializers.ValidationError("Organisation non fournie")
        
        try:
            organization = Organization.objects.get(id=organization_data['id'])
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organisation introuvable")
        
        # Générer un ID unique pour le document
        document_id = f"doc_{uuid.uuid4().hex[:12]}"
        
        # Décoder les fichiers base64
        try:
            original_pdf_data = base64.b64decode(validated_data['original_document_data'])
        except Exception as e:
            raise serializers.ValidationError(f"Erreur lors du décodage du fichier original: {str(e)}")
        
        # Créer le fichier original
        original_filename = validated_data['original_filename']
        original_file = ContentFile(original_pdf_data, name=f"{document_id}_original_{original_filename}")
        
        # Gérer le fichier actuel (optionnel)
        current_file = None
        if validated_data.get('current_document_data'):
            try:
                current_pdf_data = base64.b64decode(validated_data['current_document_data'])
                current_file = ContentFile(current_pdf_data, name=f"{document_id}_current_{original_filename}")
            except Exception as e:
                raise serializers.ValidationError(f"Erreur lors du décodage du fichier actuel: {str(e)}")
        
        # Gérer le PDF généré (optionnel)
        generated_pdf_file = None
        if validated_data.get('final_document_data'):
            try:
                generated_pdf_data = base64.b64decode(validated_data['final_document_data'])
                generated_pdf_file = ContentFile(generated_pdf_data, name=f"{document_id}_generated_{original_filename}")
            except Exception as e:
                raise serializers.ValidationError(f"Erreur lors du décodage du PDF généré: {str(e)}")
        
        # Gérer l'image de signature (optionnel)
        signature_image_file = None
        if validated_data.get('signature_image'):
            try:
                # Extraire le type MIME et les données
                signature_data = validated_data['signature_image']
                if signature_data.startswith('data:image/'):
                    header, data = signature_data.split(',', 1)
                    image_type = header.split('/')[1].split(';')[0]  # png, jpg, etc.
                    image_data = base64.b64decode(data)
                    signature_image_file = ContentFile(image_data, name=f"{document_id}_signature.{image_type}")
                else:
                    # Assume it's already base64 without header
                    image_data = base64.b64decode(signature_data)
                    signature_image_file = ContentFile(image_data, name=f"{document_id}_signature.png")
            except Exception as e:
                raise serializers.ValidationError(f"Erreur lors du décodage de l'image de signature: {str(e)}")
        
        # Extraire les données de configuration des éléments
        elements_config = validated_data.get('elements_configuration', {})
        
        # Extraire les données QR Code
        qr_config = elements_config.get('qr_code', {})
        qr_x = qr_config.get('x')
        qr_y = qr_config.get('y')
        qr_size = qr_config.get('size', 'medium')
        qr_page = qr_config.get('page', 1)
        
        # Extraire les données Signature
        sig_config = elements_config.get('signature', {})
        sig_x = sig_config.get('x')
        sig_y = sig_config.get('y')
        sig_width = sig_config.get('width')
        sig_height = sig_config.get('height')
        sig_page = sig_config.get('page', 1)
        
        # Préparer les données pour le DocumentPreparationSerializer
        preparation_data = {
            'document_id': document_id,
            'organization': organization.id,
            'prepared_by': user.id,
            'document_title': validated_data['document_title'],
            'document_description': validated_data.get('document_description', ''),
            'original_filename': original_filename,
            'original_document': original_file,
            'file_size_original': validated_data['file_size_original'],
            'preparation_notes': validated_data.get('preparation_notes', ''),
            'elements_configuration': elements_config,
            # QR Code fields
            'qr_code_x': qr_x,
            'qr_code_y': qr_y,
            'qr_code_size': qr_size,
            'qr_code_page': qr_page,
            # Signature fields
            'signature_x': sig_x,
            'signature_y': sig_y,
            'signature_width': sig_width,
            'signature_height': sig_height,
            'signature_page': sig_page,
            'status': 'prepared',
            'prepared_at': timezone.now()
        }
        
        # Ajouter les fichiers optionnels s'ils existent
        if current_file:
            preparation_data['current_document'] = current_file
        else:
            # Si pas de fichier actuel, utiliser l'original
            preparation_data['current_document'] = original_file
            
        if generated_pdf_file:
            preparation_data['generated_pdf'] = generated_pdf_file
            
        if signature_image_file:
            preparation_data['secretary_signature_image'] = signature_image_file
        
        # Utiliser le DocumentPreparationSerializer pour créer l'objet
        serializer = DocumentPreparationSerializer(data=preparation_data)
        serializer.is_valid(raise_exception=True)
        document_preparation = serializer.save()
        
        return document_preparation