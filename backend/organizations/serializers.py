from rest_framework import serializers
from .models import Organization, OrganizationMember, InvitationCode, OrganizationCertificate
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
            'is_approved', 'approval_date', 'approved_by', 'admin_count', 
            'member_count', 'user_id'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'is_approved', 'approval_date', 'approved_by']

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
        
        # S'assurer que is_approved est défini (par défaut False)
        if 'is_approved' not in validated_data:
            validated_data['is_approved'] = False
        
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


class OrganizationCertificateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les certificats d'organisation
    """
    imported_by_name = serializers.CharField(source='imported_by.full_name', read_only=True)
    subject_info = serializers.SerializerMethodField()
    issuer_info = serializers.SerializerMethodField()
    validity_info = serializers.SerializerMethodField()
    is_expired = serializers.ReadOnlyField()
    days_until_expiry = serializers.ReadOnlyField()
    
    class Meta:
        model = OrganizationCertificate
        fields = [
            'id', 'organization', 'name', 'subject_common_name', 'subject_organization',
            'subject_organizational_unit', 'subject_country', 'subject_email',
            'issuer_common_name', 'issuer_organization', 'issuer_country',
            'serial_number', 'fingerprint', 'signature_algorithm',
            'not_before', 'not_after', 'is_valid', 'key_usage',
            'imported_at', 'imported_by', 'imported_by_name', 'is_active',
            'subject_info', 'issuer_info', 'validity_info', 'is_expired', 'days_until_expiry'
        ]
        read_only_fields = ['id', 'imported_at', 'imported_by']
    
    def get_subject_info(self, obj):
        return obj.get_subject_info()
    
    def get_issuer_info(self, obj):
        return obj.get_issuer_info()
    
    def get_validity_info(self, obj):
        return obj.get_validity_info()


class OrganizationCertificateCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création de certificats d'organisation
    """
    class Meta:
        model = OrganizationCertificate
        fields = [
            'name', 'subject_common_name', 'subject_organization',
            'subject_organizational_unit', 'subject_country', 'subject_email',
            'issuer_common_name', 'issuer_organization', 'issuer_country',
            'serial_number', 'fingerprint', 'signature_algorithm',
            'not_before', 'not_after', 'is_valid', 'key_usage',
            'private_key_pem', 'public_key_pem', 'certificate_pem'
        ]


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


class InvitationCodeSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les codes d'invitation
    """
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    used_by_name = serializers.CharField(source='used_by.full_name', read_only=True)
    is_expired = serializers.ReadOnlyField()
    is_valid = serializers.ReadOnlyField()
    
    class Meta:
        model = InvitationCode
        fields = [
            'id', 'code', 'organization', 'organization_name', 'role',
            'created_by', 'created_by_name', 'used_by', 'used_by_name',
            'created_at', 'expires_at', 'used_at', 'is_active', 'is_used',
            'is_expired', 'is_valid'
        ]
        read_only_fields = [
            'id', 'code', 'created_by', 'used_by', 'created_at', 
            'expires_at', 'used_at', 'is_used', 'is_expired', 'is_valid'
        ]


class InvitationCodeCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création d'un code d'invitation
    """
    class Meta:
        model = InvitationCode
        fields = ['organization', 'role']
    
    def create(self, validated_data):
        """
        Créer un code d'invitation avec génération automatique du code
        """
        import time
        import random
        import string
        
        # Récupérer l'utilisateur depuis le contexte
        user = self.context['request'].user
        
        # Générer un code unique
        timestamp = str(int(time.time()))
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        organization_id = validated_data['organization'].id
        role = validated_data['role'].upper()
        
        # Format: INV-{orgId}-{role}-{timestamp}-{random}
        code = f"INV-{organization_id}-{role}-{timestamp}-{random_string}"
        
        # Créer le code d'invitation
        invitation_code = InvitationCode.objects.create(
            code=code,
            organization=validated_data['organization'],
            role=validated_data['role'],
            created_by=user
        )
        
        return invitation_code


class InvitationCodeValidateSerializer(serializers.Serializer):
    """
    Sérialiseur pour valider un code d'invitation
    """
    code = serializers.CharField(max_length=100)
    
    def validate_code(self, value):
        """
        Valider que le code existe et est valide
        """
        try:
            invitation_code = InvitationCode.objects.get(code=value)
            if not invitation_code.is_valid:
                if invitation_code.is_used:
                    raise serializers.ValidationError("Ce code d'invitation a déjà été utilisé.")
                elif invitation_code.is_expired:
                    raise serializers.ValidationError("Ce code d'invitation a expiré.")
                else:
                    raise serializers.ValidationError("Ce code d'invitation n'est pas actif.")
        except InvitationCode.DoesNotExist:
            raise serializers.ValidationError("Code d'invitation invalide.")
        
        return value
