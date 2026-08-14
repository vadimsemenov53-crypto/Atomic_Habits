from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Создание супер юзера"""

    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@gmail.com",
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password("7777")
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Успешно! Супер пользователь: {user.email} создан!"))
