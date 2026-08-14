from rest_framework import serializers
from rest_framework.serializers import ValidationError
from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Habit. """

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "period",
            "reward",
            "duration",
            "is_public",
        )
        read_only_fields = ("user",)

    def validate(self, attrs):
        """ Переопределение метода validate для правильного формирования структуры привычек. """
        instance = self.instance

        is_pleasant = attrs.get(
            "is_pleasant",
            instance.is_pleasant if instance else False
        )
        related_habit = attrs.get(
            "related_habit",
            instance.related_habit if instance else None
        )
        reward = attrs.get(
            "reward",
            instance.reward if instance else None
        )

        if is_pleasant and reward:
            raise ValidationError("У приятной привычки не может быть вознаграждения.")

        if is_pleasant and related_habit:
            raise ValidationError("Приятная привычка не может иметь связанную привычку.")

        if related_habit and not related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        if related_habit and self.instance and related_habit.pk == self.instance.pk:
            raise ValidationError("Привычка не может быть связана сама с собой.")

        if not is_pleasant and not related_habit and not reward:
            raise ValidationError("Полезная привычка должна иметь связанную привычку или вознаграждение.")

        if not is_pleasant and related_habit and reward:
            raise  ValidationError("Полезная привычка не может иметь одновременно связанную причку и вознаграждение.")

        return attrs
