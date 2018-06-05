from django.core.management.base import BaseCommand
# from CreateYourLaws.models import Law_Article, Law_code,
# code_block, Article_Text, Table, Cell
from CreateYourLaws.dl_law_codes.download_codes import _Main_
from django.contrib.sessions.models import Session
from datetime import date


class Command(BaseCommand):
    args = 'Arguments is not needed (yet)'
    help = 'Initialize the DB from Légifrance laws DB'

    def handle(self, *args, **options):
        self.stdout.write("Hello World")
        _Main_()
        # Session.objects.filter(expire_date__lt=date.today).delete()
