from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_information_about_start_habit():
    """ Функция отправки оповещения в чат-TG о скором начале выполнения привычки. """
    message_1 = "Напоминание до начала выполнения привычки осталось менее 10 минут."
    message_2 = "Старт! начинаем выполнять действие."
    ten_minet_ago = timezone.now() - timedelta(minutes=10)

    habits = Habit.objects.all()

    for habit in habits:
        if habit.user.tg_chat_id:
            if timezone.now() >= ten_minet_ago:
                send_telegram_message(
                    chat_id=habit.user.tg_chat_id,
                    message=message_1
                )

            elif timezone.now() == habit.time:
                send_telegram_message(
                    chat_id=habit.user.tg_chat_id,
                    message=message_2
                )