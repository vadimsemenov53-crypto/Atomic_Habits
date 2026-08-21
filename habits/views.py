import datetime
from datetime import timedelta

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginations import CustomPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


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
        """Метод переопределения получения данных."""
        return Habit.objects.filter(user=self.request.user)

    @action(detail=False, methods=("get",))
    def public(self, request):
        """Метод для отображения всех публичных привычек."""
        queryset = Habit.objects.filter(is_public=True)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def get_permissions(self):
        """Метод отвечающий за перераспределение прав доступа"""

        if self.action in ["update", "partial_update", "retrieve", "destroy"]:
            self.permission_classes = (IsOwner,)

        return super().get_permissions()

    def perform_create(self, serializer):
        """Метод отвечающий за автоматическое заполнение пользователя."""
        habit = serializer.save(user=self.request.user)
        habit.user = self.request.user

        now = timezone.localtime()
        reminder_date = timezone.localdate()  # 2026-08-19

        if now.time() >= habit.time:
            reminder_date += timedelta(days=1)

        time_next_reminder = timezone.make_aware(  # 2026-08-19T20:00:00+03:00 (Moscow - TIME_ZONE)
            datetime.datetime.combine(  # 2026-08-19T20:00:00
                reminder_date,  # 2026-08-19
                habit.time,  # "time": "20:00:00"
            )
        )

        habit.next_reminder = time_next_reminder  # 2026-08-19T20:00:00+03:00
        habit.reminder_10_sent = time_next_reminder - timedelta(minutes=10)  # 2026-08-19T19:50:00+03:00
        habit.save()
