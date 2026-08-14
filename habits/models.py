from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from config.settings import AUTH_USER_MODEL


class Habit(models.Model):
    """ Класс представления модели 'Привычка'. """
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создал",
        help_text="Укажите создателя",
    )
    place = models.CharField(
        max_length=150,
        verbose_name="Место",
        help_text="Укажите место выполнения привычки",
    )
    time = models.TimeField(
        verbose_name="Время",
        help_text="Укажите время выполнения",
    )
    action = models.CharField(
        max_length=250,
        verbose_name="Действие",
        help_text="Укажите действие для выполнения",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная",
        help_text="Укажите наличие приятно привычки",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Укажите связанную привычку",
        related_name="dependent_habits",
    )
    period = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность (раз в неделю)",
        help_text="Укажите периодичность выполнения",
    )
    reward = models.CharField(
        max_length=250,
        verbose_name="Награда",
        help_text="Укажите награду за выполнение",
        null=True,
        blank=True,
    )
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name="Время на выполнение (сек.)",
        help_text="Укажите время выполнения привычки."
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная",
        help_text="Укажите публичность",
    )

    def __str__(self):
        """ Метод строкового отображения. """
        return f'я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("place",)