from rest_framework import serializers
from django.contrib.auth import get_user_model
from validate_email import validate_email
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate(self, attrs):
        """Validate the email using py3-validate-email package and username to be alphanumeric"""
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should contain alphanumeric characters")
        if not validate_email(email_address=email, check_regex=True, check_mx=True, use_blacklist=True):
            raise serializers.ValidationError("The email address is not valid")

        return attrs

    def create(self, validated_data):
        """Create a user with validated data"""
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=150, min_length=3)
    password = serializers.CharField(
        max_length=255, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=6, read_only=True)
    tokens = serializers.CharField(
        max_length=255, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account inactive, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }
