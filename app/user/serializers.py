"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers
from core.models import Permission, Role, Book
from rest_framework.authtoken.models import Token



class RoleSerializer(serializers.ModelSerializer):
    """Serializer for the Role model."""

    # We can add permissions as a nested field or as a many-to-many relationship
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = Role
        fields = ['id', 'role_name', 'permissions']  # Updated fields, removed 'role_key' and 'user'
        read_only_fields = []  # If you want 'user' to be optional or read-only, remove it from this serializer.

class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for the Permission model."""

    class Meta:
        model = Permission
        fields = ['id', 'method', 'name', 'url', 'description']

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'role']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password and assigned role."""
        role_data = validated_data.pop('role', None)
        user = get_user_model().objects.create_user(**validated_data)

        if role_data:
            # Assign the role to the user
            user.role = role_data
            user.save()

        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)

        # Update user details
        user = super().update(instance, validated_data)

        # Update password if provided
        if password:
            user.set_password(password)
            user.save()


        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model."""

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'pages', 'language']