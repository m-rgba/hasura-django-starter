from rest_framework import serializers, status, permissions, generics, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt import authentication
from django.contrib.auth.models import User 
from api.models import profile
import requests
import logging
import json

# Hasura > JWT Specifics
class HasuraTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_name'] = user.username
        token['user_email'] = user.email
        token['https://hasura.io/jwt/claims'] = {}
        token['https://hasura.io/jwt/claims']['x-hasura-allowed-roles'] = [user.profile.role]
        token['https://hasura.io/jwt/claims']['x-hasura-default-role'] = user.profile.role
        token['https://hasura.io/jwt/claims']['x-hasura-user-id'] = str(user.id)
        return token

class HasuraTokenObtainPair(TokenObtainPairView):
    serializer_class = HasuraTokenObtainPairSerializer

class ValidateTokenRefreshSerializer(TokenRefreshSerializer):
    # Validate user account is active, and the user role matches the issued JWT
    # Based on: https://github.com/SimpleJWT/django-rest-framework-simplejwt/issues/193
    error_msg = 'No active account found with the given credentials'

    def validate(self, attrs):
        token_payload = token_backend.decode(attrs['refresh'])
        try:
            user = User.objects.get(pk=token_payload['user_id'])
        except User.DoesNotExist:
            print('User does not exist')
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )

        if not user.is_active or user.email != token_payload['user_email']:
            print('Email Does Not Exist / Non-Active')
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )

        if user.profile.role != token_payload['https://hasura.io/jwt/claims']['x-hasura-default-role']:
            # TODO: Create re-issue endpoint
            # refresh = HasuraTokenObtainPairSerializer.get_token(user)
            # return Response(data={'refresh': str(refresh), 'access': str(refresh.access_token)})
            
            print(user.profile.role)
            print(token_payload['https://hasura.io/jwt/claims']['x-hasura-default-role'])
            print('Roles Dont Match')
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )
            
        return super().validate(attrs)

class ValidateTokenRefreshView(TokenRefreshView):
    serializer_class = ValidateTokenRefreshSerializer

# Serializers
class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    tokens = serializers.SerializerMethodField()
    def get_tokens(self, user):
        refresh = HasuraTokenObtainPairSerializer.get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        return data

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'tokens')

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# Views
class RegisterUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class ChangePassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    model = User
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)