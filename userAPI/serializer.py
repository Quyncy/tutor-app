"""
Serializer for the user API view
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import *

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write-only': True,
            'min_length': 5
            }
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return User.objects.create_user(**validated_data)