import pycountry
from django.core.management.base import BaseCommand
from users.models import Country

class Command(BaseCommand):
    help = "Import all countries from pycountry package into the database"

    def handle(self, *args, **kwargs):
        countries_added = 0
        for country in pycountry.countries:
            # Avoid duplicates by checking ISO code
            if not Country.objects.filter(iso_code=country.alpha_2).exists():
                Country.objects.create(name=country.name, iso_code=country.alpha_2)
                countries_added += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully added {countries_added} countries!"))
