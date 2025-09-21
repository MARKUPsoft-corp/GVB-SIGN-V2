from django.contrib.admin import AdminSite
from django.contrib.admin.views.main import ChangeList
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import User, AuthToken


class TokenDashboard(ChangeList):
    """
    Dashboard personnalisé pour les tokens d'authentification
    """
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques des tokens
        total_tokens = AuthToken.objects.count()
        active_tokens = AuthToken.objects.filter(is_active=True).count()
        expired_tokens = AuthToken.objects.filter(
            expires_at__lt=timezone.now()
        ).count()
        
        # Tokens expirant bientôt (7 jours)
        soon_expired = AuthToken.objects.filter(
            expires_at__lte=timezone.now() + timedelta(days=7),
            expires_at__gt=timezone.now(),
            is_active=True
        ).count()
        
        # Statistiques par type de token
        token_types = AuthToken.objects.values('token_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Utilisateurs avec le plus de tokens
        top_users = User.objects.annotate(
            token_count=Count('auth_tokens')
        ).filter(token_count__gt=0).order_by('-token_count')[:10]
        
        # Tokens récents (7 derniers jours)
        recent_tokens = AuthToken.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        context.update({
            'total_tokens': total_tokens,
            'active_tokens': active_tokens,
            'expired_tokens': expired_tokens,
            'soon_expired': soon_expired,
            'token_types': token_types,
            'top_users': top_users,
            'recent_tokens': recent_tokens,
        })
        
        return context


def get_admin_stats():
    """
    Récupérer les statistiques pour l'admin
    """
    now = timezone.now()
    
    return {
        'users': {
            'total': User.objects.count(),
            'active': User.objects.filter(is_active=True).count(),
            'verified': User.objects.filter(is_verified=True).count(),
            'superusers': User.objects.filter(is_superuser=True).count(),
        },
        'tokens': {
            'total': AuthToken.objects.count(),
            'active': AuthToken.objects.filter(is_active=True).count(),
            'expired': AuthToken.objects.filter(expires_at__lt=now).count(),
            'expiring_soon': AuthToken.objects.filter(
                expires_at__lte=now + timedelta(days=7),
                expires_at__gt=now,
                is_active=True
            ).count(),
        },
        'recent_activity': {
            'new_users_week': User.objects.filter(
                created_at__gte=now - timedelta(days=7)
            ).count(),
            'new_tokens_week': AuthToken.objects.filter(
                created_at__gte=now - timedelta(days=7)
            ).count(),
        }
    }
