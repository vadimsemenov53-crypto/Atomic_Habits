from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsProfile, IsSuperUser
from users.serializer import UserSerializer, UserPublicSerializer


class UserViewSet(ModelViewSet):
    """Контроллер для модели User использующий ModelViewSet"""

    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "email",
        "first_name",
        "last_name",
        "is_active",
    ]

    @swagger_auto_schema(responses={200: UserPublicSerializer})
    def retrieve(self, request, *args, **kwargs):
        """ Переопределения метода retrieve у ModelViewSet
        (Отображение публичного UserPublicSerializer документации.) """
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return UserPublicSerializer

        if self.action == "retrieve":
            if self.request.user != self.get_object():
                return UserPublicSerializer

        return UserSerializer

    def get_permissions(self):
        """ Переопределение прав доступа для UserViewSet. """
        if self.action == "create":
            self.permission_classes = (AllowAny,)

        elif self.action in ["update", "partial_update"]:
            self.permission_classes = (IsProfile,)

        elif self.action == "destroy":
            self.permission_classes = (IsSuperUser,)

        return super().get_permissions()
