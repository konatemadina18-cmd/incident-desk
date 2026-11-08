import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Crée les comptes initiaux des enseignants."

    def handle(self, *args, **options):
        teacher_username = os.environ.get("INITIAL_TEACHER_USERNAME")
        teacher_password = os.environ.get("INITIAL_TEACHER_PASSWORD")
        admin_username = os.environ.get("INITIAL_ADMIN_USERNAME")
        admin_password = os.environ.get("INITIAL_ADMIN_PASSWORD")

        if not all([
            teacher_username,
            teacher_password,
            admin_username,
            admin_password,
        ]):
            raise CommandError("Les variables de création des comptes sont incomplètes.")

        User = get_user_model()

        if teacher_username == admin_username:
            raise CommandError("Les noms des deux comptes doivent être différents.")

        with transaction.atomic():
            if User.objects.filter(username=teacher_username).exists():
                self.stdout.write("Le compte enseignant existe déjà : aucune modification.")
            else:
                User.objects.create_user(
                    username=teacher_username,
                    password=teacher_password,
                )
                self.stdout.write(self.style.SUCCESS("Compte enseignant créé."))

            admin = User.objects.filter(username=admin_username).first()

            if admin:
                if not admin.is_superuser:
                    raise CommandError(
                        "Le compte administrateur existe déjà sans droits superutilisateur. "
                        "Aucune modification automatique effectuée."
                    )
                self.stdout.write("Le compte administrateur existe déjà : aucune modification.")
            else:
                User.objects.create_superuser(
                    username=admin_username,
                    password=admin_password,
                )
                self.stdout.write(self.style.SUCCESS("Compte administrateur créé."))

        self.stdout.write(self.style.SUCCESS("Opération terminée."))