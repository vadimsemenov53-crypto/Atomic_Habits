from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    """Тест кейс контроллера UserViewSet."""

    def setUp(self):
        """Начальный сет-ап с тестовыми данными."""
        self.user1 = User.objects.create(email="admin@gmail.com", first_name="example")
        self.user1.set_password("7777")
        self.user1.save()

        self.user2 = User.objects.create(email="admin777@gmail.com")
        self.user2.set_password("7777")
        self.user2.save()

        self.user3 = User.objects.create(email="superuser@gmail.com")
        self.user3.is_superuser = True
        self.user3.set_password("7777")
        self.user3.save()

    def test_user_register(self):
        """Тестирование получаемых данных для -> users:user-create."""
        url = reverse("users:users-list")
        data = {"email": "example@gmail.com", "password": "7777"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.all().count(), 4)

        self.assertEqual(response.data["email"], data["email"])

    def test_get_token_for_user(self):
        """Тестирование получаемых данных для -> users:login."""
        url = reverse("users:login")
        data = {"email": "admin@gmail.com", "password": "7777"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())
        self.assertTrue(response.data["access"])
        self.assertTrue(response.data["refresh"])

    def test_get_token_wrong_password(self):
        """Тестирование получаемых данных для -> users:login."""
        url = reverse("users:login")
        data = {"email": "admin@gmail.com", "password": "wrong_pass"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(response.json(), {"detail": "Не найдено активной учетной записи с указанными данными"})

    def test_get_info_profile(self):
        """Тестирование получаемых данных для -> users:users-detail."""
        self.client.force_authenticate(user=self.user1)

        url = reverse("users:users-detail", args=(self.user1.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user1.email)
        self.assertEqual(data.get("first_name"), self.user1.first_name)
        self.assertIn("tg_chat_id", data)

    def test_get_info_another_profile(self):
        """Тестирование получаемых данных для -> users:users-detail."""
        self.client.force_authenticate(user=self.user1)

        url = reverse("users:users-detail", args=(self.user2.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user2.email)
        self.assertNotIn("first_name", data)
        self.assertNotIn("tg_chat_id", data)

    def test_update_profile(self):
        """Тестирование получаемых данных для -> users:users-detail."""
        self.client.force_authenticate(user=self.user2)

        url1 = reverse("users:users-detail", args=(self.user2.pk,))
        response1 = self.client.get(url1)
        data = response1.json()

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user2.email)
        self.assertEqual(data.get("first_name"), "")
        self.assertEqual(data.get("tg_chat_id"), None)

        url2 = reverse("users:users-detail", args=(self.user2.pk,))
        update_data = {"first_name": "example", "tg_chat_id": "2525"}
        response2 = self.client.patch(url2, update_data)
        data = response2.json()

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("first_name"), update_data["first_name"])
        self.assertEqual(data.get("tg_chat_id"), update_data["tg_chat_id"])

    def test_delete_user(self):
        """Тестирование получаемых данных для -> users:users-detail (DELETE)."""
        self.client.force_authenticate(user=self.user3)

        self.assertEqual(User.objects.all().count(), 3)

        url = reverse("users:users-detail", args=(self.user2.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 2)
