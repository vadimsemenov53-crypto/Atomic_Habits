from datetime import timedelta
from celery import shared_task
from django.db.models import Q
from django.utils import timezone
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_information_about_start_habit():
    """ Функция отправки оповещения в чат-TG о скором начале выполнения привычки. """
    now = timezone.now()

    habits = Habit.objects.filter(
                Q(reminder_10_sent__lte=now) | Q(next_reminder__lte=now)
    ).select_related("user")

    for habit in habits:
        if habit.user.tg_chat_id:

            if habit.reminder_10_sent <= now < habit.next_reminder:
                send_telegram_message(
                    chat_id=habit.user.tg_chat_id,
                    message=f"Напоминаем! Через 10 минут: {habit.action}."
                )
                habit.reminder_10_sent += timedelta(days=habit.period)
                habit.save(update_fields=["reminder_10_sent"])

            elif habit.next_reminder <= now:
                send_telegram_message(
                    chat_id=habit.user.tg_chat_id,
                    message=f"Старт! Приступайте к выполнению: {habit.action} - {habit.duration} секунд."
                )
                habit.next_reminder += timedelta(days=habit.period)
                habit.save(update_fields=["next_reminder"])