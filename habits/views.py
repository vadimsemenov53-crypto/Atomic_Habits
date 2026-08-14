from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from habits.models import Habit
from habits.paginations import CustomPagination


class HabitViewSet(ModelViewSet):
    """Контроллер для модели Habit использующий ModelViewSet"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """ Метод переопределения получения данных. """
        return Habit.objects.filter(
            Q(user=self.request.user) | Q(is_public=True)
        )

    def perform_create(self, serializer):
        """Метод отвечающий за автоматическое заполнение владельца"""
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()