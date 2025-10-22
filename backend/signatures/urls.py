from django.urls import path
from . import views

app_name = 'signatures'

urlpatterns = [
    # Document preparation endpoints
    path('document-preparation/create/', views.create_document_preparation, name='create_document_preparation'),
    path('document-preparation/', views.get_document_preparations, name='get_document_preparations'),
    path('document-preparation/<uuid:preparation_id>/', views.get_document_preparation, name='get_document_preparation'),
    path('document-preparation/<uuid:preparation_id>/save-signature/', views.save_document_signature, name='save_document_signature'),
    path('document-preparation/<uuid:preparation_id>/advance/', views.advance_workflow, name='advance_workflow'),
    
    # Pending signatures
    path('pending-signatures/', views.get_pending_signatures, name='get_pending_signatures'),
    
    # Signed documents
    path('signed-documents/', views.get_signed_documents, name='get_signed_documents'),
    
    # Signature verification
    path('verify-signature/<str:document_id>/', views.verify_signature_by_document_id, name='verify_signature_by_document_id'),
    
    # PDF preview endpoint (sans restrictions X-Frame-Options)
    path('pdf-preview/<uuid:document_id>/<str:file_type>/', views.serve_pdf_for_preview, name='serve_pdf_for_preview'),
    
    # Bulk signatures endpoint
    path('bulk-create/', views.bulk_create_signatures, name='bulk_create_signatures'),
]