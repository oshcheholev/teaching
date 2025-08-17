"""
User-related API Views
======================

This module contains views related to user management and authentication.
"""

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user account.
    
    This view allows user registration without authentication required.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
