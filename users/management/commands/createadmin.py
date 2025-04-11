from django.core.management.base import BaseCommand
from users.models import User


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         user = User.objects.create(
#             email='admin@email.com',
#         )
#
#         user.set_password('1234qwer')
#
#         user.is_active = True
#         user.is_staff = True
#         user.is_superuser = True
#
#         user.save()
#
#         self.stdout.write(self.style.SUCCESS(f'Successfully created admin user with {user.email}!'))
class Command(BaseCommand):
    help = 'Создает администратора'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email администратора')
        parser.add_argument('password', type=str, help='Пароль администратора')

    def handle(self, *args, **options):
        # User = get_user_model()
        email = options['email']
        password = options['password']

        user = User(email=email)
        user.set_password(password)  # Хэшируем пароль
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created admin user with {user.email}!'))
