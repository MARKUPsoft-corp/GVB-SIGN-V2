from rest_framework import serializers
from .models import Organization, OrganizationMember
from authentication.serializers import UserSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les organisations
    """
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    admin_count = serializers.ReadOnlyField()
    member_count = serializers.ReadOnlyField()
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'description', 'email', 'phone', 'address', 
            'website', 'organization_type', 'sector', 'created_at', 
            'updated_at', 'created_by', 'created_by_name', 'is_active',
            'admin_count', 'member_count', 'user_id'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def create(self, validated_data):
        """
        Créer une organisation et assigner l'utilisateur comme administrateur
        """
        print(f"🔍 === DÉBUT DE LA CRÉATION D'ORGANISATION ===")
        
        # Récupérer l'ID de l'utilisateur depuis les données validées
        user_id = validated_data.pop('user_id', None)
        print(f"🔍 User ID reçu depuis le frontend: {user_id}")
        
        if not user_id:
            print(f"🔍 ERREUR: Aucun user_id fourni!")
            raise serializers.ValidationError("ID utilisateur requis")
        
        # Récupérer l'utilisateur depuis la base de données
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(id=user_id)
            print(f"🔍 Utilisateur récupéré depuis la DB: {user}")
            print(f"🔍 ID utilisateur: {user.id}")
            print(f"🔍 Email utilisateur: {user.email}")
            print(f"🔍 Nom complet utilisateur: {user.full_name}")
        except User.DoesNotExist:
            print(f"🔍 ERREUR: Utilisateur avec ID {user_id} non trouvé!")
            raise serializers.ValidationError(f"Utilisateur avec ID {user_id} non trouvé")
        
        # Ajouter l'utilisateur aux données validées
        validated_data['created_by'] = user
        
        print(f"🔍 Données validées AVANT création: {validated_data}")
        print(f"🔍 Clés des données validées: {list(validated_data.keys())}")
        
        try:
            # Créer l'organisation
            print(f"🔍 Tentative de création de l'organisation...")
            organization = Organization.objects.create(**validated_data)
            print(f"🔍 Organisation créée avec succès: {organization}")
            print(f"🔍 ID organisation: {organization.id}")
            print(f"🔍 Créateur organisation: {organization.created_by}")
            
        except Exception as e:
            print(f"🔍 ERREUR lors de la création de l'organisation: {str(e)}")
            print(f"🔍 Type d'erreur: {type(e)}")
            raise e
        
        # Créer l'adhésion de l'utilisateur comme administrateur
        try:
            print(f"🔍 Création de l'adhésion...")
            OrganizationMember.objects.create(
                organization=organization,
                user=user,
                role='admin'
            )
            print(f"🔍 Membre créé pour l'utilisateur")
        except Exception as e:
            print(f"🔍 ERREUR lors de la création du membre: {str(e)}")
            raise e
        
        # Mettre à jour l'utilisateur pour qu'il appartienne à cette organisation
        try:
            print(f"🔍 Mise à jour de l'utilisateur...")
            user.organization = organization
            user.role = 'admin'
            user.save()
            print(f"🔍 Utilisateur mis à jour avec l'organisation")
        except Exception as e:
            print(f"🔍 ERREUR lors de la mise à jour de l'utilisateur: {str(e)}")
            raise e
        
        print(f"🔍 === FIN DE LA CRÉATION D'ORGANISATION ===")
        return organization


class OrganizationMemberSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les membres d'organisation
    """
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    invited_by_name = serializers.CharField(source='invited_by.full_name', read_only=True)
    
    class Meta:
        model = OrganizationMember
        fields = [
            'id', 'organization', 'user', 'user_name', 'user_email',
            'role', 'joined_at', 'invited_by', 'invited_by_name'
        ]
        read_only_fields = ['id', 'joined_at', 'invited_by']


class OrganizationCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création d'organisation
    """
    class Meta:
        model = Organization
        fields = [
            'name', 'description', 'email', 'phone', 'address',
            'website', 'organization_type', 'sector'
        ]

    def validate_name(self, value):
        """
        Valider que le nom de l'organisation est unique
        """
        if Organization.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Une organisation avec ce nom existe déjà.")
        return value

    def validate_email(self, value):
        """
        Valider que l'email de l'organisation est unique
        """
        if Organization.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Une organisation avec cet email existe déjà.")
        return value


class OrganizationListSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la liste des organisations (version simplifiée)
    """
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    member_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'description', 'organization_type', 'sector',
            'created_at', 'created_by_name', 'member_count', 'is_active'
        ]
