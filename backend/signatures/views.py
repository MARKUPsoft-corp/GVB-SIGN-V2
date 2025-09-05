from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser
from django.shortcuts import get_object_or_404
from .models import DocumentSignature
from .serializers import (
    DocumentSignatureSerializer,
    DocumentSignatureListSerializer,
    DocumentSignatureDetailSerializer
)

class DocumentSignatureCreateView(generics.CreateAPIView):
    """
    Vue pour créer une nouvelle signature de document
    """
    queryset = DocumentSignature.objects.all()
    serializer_class = DocumentSignatureSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            signature = serializer.save()
            return Response({
                'success': True,
                'message': 'Signature enregistrée avec succès',
                'signature_id': str(signature.id),
                'document_id': signature.document_id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': 'Erreur lors de l\'enregistrement de la signature',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class DocumentSignatureListView(generics.ListAPIView):
    """
    Vue pour lister les signatures de l'utilisateur connecté
    """
    serializer_class = DocumentSignatureListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DocumentSignature.objects.filter(user=self.request.user)

class DocumentSignatureDetailView(generics.RetrieveAPIView):
    """
    Vue pour récupérer les détails d'une signature
    """
    serializer_class = DocumentSignatureDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DocumentSignature.objects.filter(user=self.request.user)

class DocumentSignatureBulkCreateView(generics.CreateAPIView):
    """
    Vue pour créer plusieurs signatures en une seule requête
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    
    def create(self, request, *args, **kwargs):
        # Logs pour diagnostiquer l'authentification
        print(f"=== DIAGNOSTIC BACKEND ===")
        print(f"User authentifié: {request.user}")
        print(f"User ID: {request.user.id if request.user.is_authenticated else 'Non authentifié'}")
        print(f"User email: {request.user.email if request.user.is_authenticated else 'Non authentifié'}")
        print(f"Session key: {request.session.session_key}")
        print(f"Cookies: {request.COOKIES}")
        
        signatures_data = request.data.get('signatures', [])
        
        if not signatures_data:
            return Response({
                'success': False,
                'message': 'Aucune signature fournie'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        created_signatures = []
        errors = []
        
        for i, signature_data in enumerate(signatures_data):
            serializer = DocumentSignatureSerializer(data=signature_data, context={'request': request})
            if serializer.is_valid():
                try:
                    signature = serializer.save()
                    created_signatures.append({
                        'index': i,
                        'signature_id': str(signature.id),
                        'document_id': signature.document_id,
                        'status': 'created'
                    })
                except Exception as e:
                    errors.append({
                        'index': i,
                        'document_id': signature_data.get('document_id', 'unknown'),
                        'error': str(e)
                    })
            else:
                errors.append({
                    'index': i,
                    'document_id': signature_data.get('document_id', 'unknown'),
                    'errors': serializer.errors
                })
        
        response_data = {
            'success': len(created_signatures) > 0,
            'message': f'{len(created_signatures)} signature(s) créée(s), {len(errors)} erreur(s)',
            'created_signatures': created_signatures,
            'errors': errors,
            'total_processed': len(signatures_data),
            'total_created': len(created_signatures),
            'total_errors': len(errors)
        }
        
        # Retourner 201 si au moins une signature a été créée, 400 sinon
        status_code = status.HTTP_201_CREATED if created_signatures else status.HTTP_400_BAD_REQUEST
        
        return Response(response_data, status=status_code)