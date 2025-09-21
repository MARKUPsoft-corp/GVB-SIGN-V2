from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from .models import AuthToken


class TokenAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware pour l'authentification par token
    """
    
    def process_request(self, request):
        """
        Authentifier l'utilisateur via le token dans les headers
        """
        # Exclure l'admin Django et les URLs statiques
        if (request.path.startswith('/admin/') or 
            request.path.startswith('/static/') or 
            request.path.startswith('/media/')):
            return None
        
        # Récupérer le token depuis les headers Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header.startswith('Bearer '):
            token = auth_header.replace('Bearer ', '')
            
            # Vérifier le token en base de données
            auth_token = AuthToken.get_valid_token(token)
            
            if auth_token:
                # Authentifier l'utilisateur
                request.user = auth_token.user
                request.auth_token = auth_token
                print(f"🔐 Utilisateur authentifié via token: {auth_token.user.email}")
            else:
                # Token invalide ou expiré
                request.user = AnonymousUser()
                request.auth_token = None
                print(f"❌ Token invalide ou expiré: {token[:10]}...")
        else:
            # Pas de token fourni
            request.user = AnonymousUser()
            request.auth_token = None
        
        return None
