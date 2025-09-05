from rest_framework import serializers
from .models import DocumentSignature
from django.core.files.base import ContentFile
import base64
import json

class DocumentSignatureSerializer(serializers.ModelSerializer):
    """
    Serializer pour créer une nouvelle signature de document
    """
    # Champs pour recevoir les fichiers en base64
    original_document_base64 = serializers.CharField(write_only=True)
    signed_document_base64 = serializers.CharField(write_only=True)
    
    class Meta:
        model = DocumentSignature
        fields = [
            'id', 'document_id', 'signer_full_name', 'original_filename',
            'document_hash', 'public_key', 'signature', 'signature_timestamp',
            'file_size_original', 'file_size_signed', 'execution_time',
            'original_document_base64', 'signed_document_base64',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Extraire les données base64
        original_doc_b64 = validated_data.pop('original_document_base64')
        signed_doc_b64 = validated_data.pop('signed_document_base64')
        
        # Décoder les fichiers base64
        try:
            original_doc_data = base64.b64decode(original_doc_b64)
            signed_doc_data = base64.b64decode(signed_doc_b64)
        except Exception as e:
            raise serializers.ValidationError(f"Erreur lors du décodage base64: {str(e)}")
        
        # Créer les fichiers
        original_filename = validated_data.get('original_filename', 'document.pdf')
        
        original_file = ContentFile(
            original_doc_data,
            name=f"original_{validated_data['document_id']}_{original_filename}"
        )
        signed_file = ContentFile(
            signed_doc_data,
            name=f"signed_{validated_data['document_id']}_{original_filename}"
        )
        
        # Ajouter l'utilisateur depuis le contexte de la requête
        validated_data['user'] = self.context['request'].user
        
        # Créer l'instance
        signature = DocumentSignature.objects.create(
            original_document=original_file,
            signed_document=signed_file,
            **validated_data
        )
        
        return signature

class DocumentSignatureListSerializer(serializers.ModelSerializer):
    """
    Serializer pour lister les signatures (sans les gros fichiers)
    """
    user_email = serializers.CharField(source='user.email', read_only=True)
    is_verified = serializers.ReadOnlyField()
    
    class Meta:
        model = DocumentSignature
        fields = [
            'id', 'document_id', 'signer_full_name', 'user_email',
            'original_filename', 'signature_timestamp', 'created_at',
            'file_size_original', 'file_size_signed', 'execution_time',
            'is_verified'
        ]

class DocumentSignatureDetailSerializer(serializers.ModelSerializer):
    """
    Serializer pour les détails d'une signature (avec toutes les infos)
    """
    user_email = serializers.CharField(source='user.email', read_only=True)
    is_verified = serializers.ReadOnlyField()
    original_document_url = serializers.SerializerMethodField()
    signed_document_url = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentSignature
        fields = [
            'id', 'document_id', 'signer_full_name', 'user_email',
            'original_filename', 'document_hash', 'public_key', 'signature',
            'signature_timestamp', 'created_at', 'updated_at',
            'file_size_original', 'file_size_signed', 'execution_time',
            'is_verified', 'original_document_url', 'signed_document_url'
        ]
    
    def get_original_document_url(self, obj):
        request = self.context.get('request')
        if obj.original_document and request:
            return request.build_absolute_uri(obj.original_document.url)
        return None
    
    def get_signed_document_url(self, obj):
        request = self.context.get('request')
        if obj.signed_document and request:
            return request.build_absolute_uri(obj.signed_document.url)
        return None
