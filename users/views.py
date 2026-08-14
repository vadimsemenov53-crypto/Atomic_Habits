from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.permissions import IsProfile
from users.serializer import UserSerializer


class UserViewSet(ModelViewSet):
    """Контроллер для модели User использующий ModelViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "email",
        "first_name",
        "last_name",
        "is_active",
    ]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)

        elif self.action in ["update", "partial_update"]:
            self.permission_classes = (IsProfile,)

        return super().get_permissions()