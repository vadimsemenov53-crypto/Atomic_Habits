from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from habits.models import Habit
from habits.paginations import CustomPagination
from habits.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    """Контроллер для модели Habit использующий ModelViewSet"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ("period",)
    filterset_fields = [
        "place",
        "action",
        "reward",
    ]

    def get_queryset(self):
        """ Метод переопределения получения данных. """
        return Habit.objects.filter(
            Q(user=self.request.user) | Q(is_public=True)
        )

    def perform_create(self, serializer):
        """Метод отвечающий за автоматическое заполнение пользователя."""
        habit = serializer.save(user=self.request.user)
        habit.user = self.request.user
        habit.save()