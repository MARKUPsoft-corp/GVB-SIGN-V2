from django.urls import path
from .views import (
    DocumentSignatureCreateView,
    DocumentSignatureListView,
    DocumentSignatureDetailView,
    DocumentSignatureBulkCreateView
)

app_name = 'signatures'

urlpatterns = [
    # Créer une signature
    path('create/', DocumentSignatureCreateView.as_view(), name='create'),
    
    # Créer plusieurs signatures en une fois
    path('bulk-create/', DocumentSignatureBulkCreateView.as_view(), name='bulk-create'),
    
    # Lister les signatures de l'utilisateur
    path('list/', DocumentSignatureListView.as_view(), name='list'),
    
    # Détails d'une signature
    path('<uuid:pk>/', DocumentSignatureDetailView.as_view(), name='detail'),
]
