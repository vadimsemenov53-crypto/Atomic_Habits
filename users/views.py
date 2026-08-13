from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializer import UserSerializer


class UserViewSet(ModelViewSet):
    """Контроллер для модели User использующий ModelViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer