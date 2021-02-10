from rest_framework import serializers
from django.contrib.auth import get_user_model
from validate_email import validate_email
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


class EmailVerification(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']
