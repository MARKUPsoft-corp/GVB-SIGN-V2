from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription des utilisateurs
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password')

    def validate(self, attrs):
        """Validation personnalisée"""
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "Les mots de passe ne correspondent pas."
            })
        return attrs

    def validate_email(self, value):
        """Validation de l'email"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un utilisateur avec cet email existe déjà.")
        return value

    def create(self, validated_data):
        """Création d'un nouvel utilisateur"""
        validated_data.pop('confirm_password')
        
        # Générer un nom d'utilisateur unique basé sur l'email
        email = validated_data['email']
        username = email.split('@')[0]
        counter = 1
        original_username = username
        
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1
            
        validated_data['username'] = username
        
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer pour la connexion des utilisateurs
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Validation des identifiants"""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Authentifier directement avec l'email (USERNAME_FIELD)
            user = authenticate(username=email, password=password)
            
            if not user:
                raise serializers.ValidationError("Identifiants invalides.")
            
            if not user.is_active:
                raise serializers.ValidationError("Ce compte est désactivé.")
                
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("Email et mot de passe requis.")


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour les informations utilisateur
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name', 'is_verified', 'created_at')
        read_only_fields = ('id', 'is_verified', 'created_at')
