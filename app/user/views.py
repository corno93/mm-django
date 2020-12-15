from rest_framework import generics

from . import serializers


class CreateUserView(generics.CreateAPIView):
    """create new user"""

    serializer_class = serializers.UserSerializer
