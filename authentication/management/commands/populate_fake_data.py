import random
from django.core.management.base import BaseCommand
from faker import Faker
from authentication.models import CustomUser, Contact, SpamReport  # Replace 'your_app' with the actual app name

class Command(BaseCommand):
    help = 'Populate the database with fake data for CustomUser, Contact, and SpamReport models'

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write(self.style.SUCCESS('Populating CustomUsers...'))
        for _ in range(50):  
            name = fake.name()
            phone_number = fake.phone_number()
            email = fake.email()

            # Avoid creating duplicate phone numbers
            while CustomUser.objects.filter(phone_number=phone_number).exists():
                phone_number = fake.phone_number()

            user = CustomUser.objects.create(
                name=name,
                phone_number=phone_number,
                email=email,
                is_active=True,
                is_staff=False
            )
            self.stdout.write(self.style.SUCCESS(f'Created user: {name} with phone number: {phone_number}'))

            self.stdout.write(self.style.SUCCESS(f'Populating Contacts for {name}...'))
            for _ in range(random.randint(1, 10)):  
                contact_name = fake.name()
                contact_phone = fake.phone_number()
                Contact.objects.create(
                    user=user,
                    name=contact_name,
                    phone_number=contact_phone
                )
                self.stdout.write(self.style.SUCCESS(f'Created contact: {contact_name} with phone number: {contact_phone}'))

            self.stdout.write(self.style.SUCCESS(f'Populating SpamReports for {name}...'))
            for _ in range(random.randint(0, 15)):  
                spam_phone = fake.phone_number()
                SpamReport.objects.create(
                    reported_by=user,
                    phone_number=spam_phone
                )
                self.stdout.write(self.style.SUCCESS(f'Created spam report for: {spam_phone}'))

        self.stdout.write(self.style.SUCCESS('Fake data population complete!'))
