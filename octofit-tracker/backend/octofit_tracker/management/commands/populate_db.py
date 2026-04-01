from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'
    
    def handle(self, *args, **options):
        # Add your test data population logic here
        self.stdout.write(self.style.SUCCESS('Successfully populated the octofit_db database with test data'))
