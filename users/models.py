from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для представления пользователей сервиса."""

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите адрес эл.почты")
    tg_chat_id = models.CharField(
        max_length=50,
        verbose_name="Телеграмм chat-id",
        help_text="Укажите телеграмм chat-id",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
