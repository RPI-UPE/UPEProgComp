from django.core.management.base import BaseCommand
from progcomp.account.models import Profile
from django.contrib.auth.models import User


class Command(BaseCommand):
    can_import_settings = True
    help = 'cleans the database by removing all users, submissions, and gradings.'
    

    def handle(self, *args, **options):
        Profile.objects.all().delete()
        User.objects.all().filter(is_staff=False).delete()

