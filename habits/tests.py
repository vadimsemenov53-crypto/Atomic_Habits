import datetime

from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """ Тест кейс контроллера HabitViewSet. """

    def setUp(self):
        """Начальный сет-ап с тестовыми данными."""
        self.user = User.objects.create(email="admin@gmail.com")
        self.habit_1 = Habit.objects.create(
            user=self.user,
            place="Работа",
            time="14:00",
            action="Разминка",
            period="2",
            duration=120,
            is_public=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        """Тестирование получаемых данных для -> habits:habits_data-list."""
        url = reverse("habits:habits_data-list")
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit_1.id,
                    "user": self.user.id,
                    "place": "Работа",
                    "time": "14:00:00",
                    "action": "Разминка",
                    "is_pleasant": False,
                    "related_habit": None,
                    "period": 2,
                    "reward": None,
                    "duration": 120,
                    "is_public": True,
                    "next_reminder": None,
                    "reminder_10_sent": None
                },
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)
        self.assertTrue(Habit.objects.all().exists())
        self.assertEqual(data, result)


    def test_habit_retrieve(self):
        """Тестирование получаемых данных для -> habits:habits_data-detail."""
        url = reverse("habits:habits_data-detail", args=(self.habit_1.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit_1.action)


    def test_course_create(self):
        """Тестирование создания привычки для -> habits:habits_data-list."""
        url = reverse("habits:habits_data-list")
        data = {
            "place": "Дом",
            "time": "08:00",
            "action": "Попить чай",
            "is_pleasant": True,
            "period": "1",
            "duration": 120,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Habit.objects.all().count(), 2)

        self.assertEqual(response.data["place"], data["place"])
