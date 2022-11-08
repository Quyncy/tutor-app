"""
Views für die User API
"""

from rest_framework import generics

from userAPI.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Erstellt einen neuen User im System"""
    serializer_class = UserSerializer

