# myapp/management/commands/generate_fake_data.py

import random
from django.core.management.base import BaseCommand
from faker import Faker
from weather_app.models import City


class Command(BaseCommand):
    help = 'Generate fake user profiles'

    def handle(self, *args, **kwargs):
        fake = Faker()
        number_of_profiles = 20
        for _ in range(number_of_profiles):
            City.objects.create(
                name=fake.text(max_nb_chars=50),
                description=fake.text()[:255]
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {number_of_profiles} Cities.'))

#python manage.py generate_fake_data
#source myproject/bin/activate
#python manage.py loaddata weather_app/fixtures/test_data.json
