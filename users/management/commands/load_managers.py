from django.core.management.base import BaseCommand
from django.core.management import call_command
from users.models import User
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Добавление данных в БД из фикстур"

    def handle(self, *args, **options):
        User.objects.all().delete()
        Group.objects.all().delete()

        call_command("loaddata", "groups_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Группы пользователей загружены из фикстур успешно"))
        call_command("loaddata", "managers_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Участники группы менеджеров загружены из фикстур успешно"))
