from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .models import User


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_user(request):
    """
    Endpoint pour l'inscription des utilisateurs
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user_data = UserSerializer(user).data
        
        return Response({
            'success': True,
            'message': 'Inscription réussie !',
            'user': user_data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Erreur lors de l\'inscription',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_user(request):
    """
    Endpoint pour la connexion des utilisateurs
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        user_data = UserSerializer(user).data
        
        return Response({
            'success': True,
            'message': 'Connexion réussie !',
            'user': user_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Erreur lors de la connexion',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    """
    Endpoint pour la déconnexion des utilisateurs
    """
    logout(request)
    return Response({
        'success': True,
        'message': 'Déconnexion réussie !'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_profile(request):
    """
    Endpoint pour récupérer le profil utilisateur
    """
    if request.user.is_authenticated:
        user_data = UserSerializer(request.user).data
        return Response({
            'success': True,
            'user': user_data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Utilisateur non authentifié'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_email(request):
    """
    Endpoint pour vérifier si un email existe déjà
    """
    email = request.GET.get('email')
    
    if not email:
        return Response({
            'success': False,
            'message': 'Email requis'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    exists = User.objects.filter(email=email).exists()
    
    return Response({
        'success': True,
        'exists': exists
    }, status=status.HTTP_200_OK)