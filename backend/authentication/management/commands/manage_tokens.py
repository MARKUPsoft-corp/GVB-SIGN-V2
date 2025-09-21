from django.core.management.base import BaseCommand
from django.utils import timezone
from authentication.models import AuthToken, User
from datetime import timedelta


class Command(BaseCommand):
    help = 'Gérer les tokens d\'authentification'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['cleanup', 'stats', 'deactivate-user', 'list-user-tokens'],
            required=True,
            help='Action à effectuer'
        )
        parser.add_argument(
            '--user-email',
            type=str,
            help='Email de l\'utilisateur (pour certaines actions)'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Nombre de jours pour le nettoyage (défaut: 30)'
        )

    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'cleanup':
            self.cleanup_tokens(options['days'])
        elif action == 'stats':
            self.show_stats()
        elif action == 'deactivate-user':
            if not options['user_email']:
                self.stdout.write(
                    self.style.ERROR('--user-email est requis pour cette action')
                )
                return
            self.deactivate_user_tokens(options['user_email'])
        elif action == 'list-user-tokens':
            if not options['user_email']:
                self.stdout.write(
                    self.style.ERROR('--user-email est requis pour cette action')
                )
                return
            self.list_user_tokens(options['user_email'])

    def cleanup_tokens(self, days):
        """Nettoyer les tokens expirés"""
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Tokens expirés
        expired_tokens = AuthToken.objects.filter(expires_at__lt=timezone.now())
        expired_count = expired_tokens.count()
        expired_tokens.delete()
        
        # Tokens anciens inactifs
        old_inactive = AuthToken.objects.filter(
            is_active=False,
            created_at__lt=cutoff_date
        )
        old_count = old_inactive.count()
        old_inactive.delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Nettoyage terminé:\n'
                f'   - {expired_count} tokens expirés supprimés\n'
                f'   - {old_count} tokens inactifs anciens supprimés'
            )
        )

    def show_stats(self):
        """Afficher les statistiques des tokens"""
        now = timezone.now()
        
        total_tokens = AuthToken.objects.count()
        active_tokens = AuthToken.objects.filter(is_active=True).count()
        expired_tokens = AuthToken.objects.filter(expires_at__lt=now).count()
        soon_expired = AuthToken.objects.filter(
            expires_at__lte=now + timedelta(days=7),
            expires_at__gt=now,
            is_active=True
        ).count()
        
        # Par type
        access_tokens = AuthToken.objects.filter(token_type='access').count()
        refresh_tokens = AuthToken.objects.filter(token_type='refresh').count()
        api_tokens = AuthToken.objects.filter(token_type='api').count()
        
        # Utilisateurs avec tokens
        users_with_tokens = User.objects.filter(auth_tokens__isnull=False).distinct().count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'📊 Statistiques des Tokens:\n'
                f'   Total: {total_tokens}\n'
                f'   Actifs: {active_tokens}\n'
                f'   Expirés: {expired_tokens}\n'
                f'   Expirent bientôt: {soon_expired}\n'
                f'   \n'
                f'   Par type:\n'
                f'   - Access: {access_tokens}\n'
                f'   - Refresh: {refresh_tokens}\n'
                f'   - API: {api_tokens}\n'
                f'   \n'
                f'   Utilisateurs avec tokens: {users_with_tokens}'
            )
        )

    def deactivate_user_tokens(self, user_email):
        """Désactiver tous les tokens d'un utilisateur"""
        try:
            user = User.objects.get(email=user_email)
            tokens = AuthToken.objects.filter(user=user, is_active=True)
            count = tokens.count()
            
            if count > 0:
                tokens.update(is_active=False)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {count} token(s) désactivé(s) pour {user_email}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Aucun token actif trouvé pour {user_email}')
                )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Utilisateur {user_email} non trouvé')
            )

    def list_user_tokens(self, user_email):
        """Lister les tokens d'un utilisateur"""
        try:
            user = User.objects.get(email=user_email)
            tokens = AuthToken.objects.filter(user=user).order_by('-created_at')
            
            if tokens.exists():
                self.stdout.write(
                    self.style.SUCCESS(f'🔑 Tokens pour {user_email}:')
                )
                for token in tokens:
                    status = '✅ Actif' if token.is_active and not token.is_expired() else '❌ Inactif/Expiré'
                    self.stdout.write(
                        f'   - {token.token[:8]}...{token.token[-8:]} '
                        f'({token.token_type}) - {status} - '
                        f'Créé: {token.created_at.strftime("%Y-%m-%d %H:%M")}'
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Aucun token trouvé pour {user_email}')
                )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Utilisateur {user_email} non trouvé')
            )
