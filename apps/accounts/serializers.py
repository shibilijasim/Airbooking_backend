from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser

from django.contrib.auth import get_user_model

User = get_user_model()

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'approval_status', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # approval_status='Pending' by default
        user = CustomUser.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Allow superusers to log in; block regular users until approved
        if not self.user.is_staff and self.user.approval_status != 'Approved':
            raise AuthenticationFailed("Account pending admin approval or rejected.")

        # Include role info in token response so React knows where to redirect
        data['username'] = self.user.username
        data['is_staff'] = self.user.is_staff
        data['approval_status'] = self.user.approval_status
        return data


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'is_active', 'approval_status', 'date_joined')