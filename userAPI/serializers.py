"""
Serializer for the user API view
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import *
import rest_framework
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer für den User"""
    class Meta:
        model = get_user_model()
        # is_superuser, usw. nicht gewollt, das es verändert wird
        fields = ['email', 'vorname', 'nachname', 'role', 'password', ]
        extra_kwargs = {'password': {'write_only':True, 'min_length': 5,}}

    def create(self, validated_data):
        """Erstellt und returnt einen User mit verschlüsselten Passwort"""
        return get_user_model().objects.create_user(**validated_data)