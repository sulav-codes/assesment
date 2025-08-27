from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample users for testing'

    def handle(self, *args, **options):
        sample_users = [
            {
                'email': 'john.doe@example.com',
                'full_name': 'John Doe',
                'contact': '1234567890',
                'company': 'Tech Corp',
                'address': '123 Main St, New York, NY',
                'industry': 'Technology',
                'password': 'testpass123'
            },
            {
                'email': 'jane.smith@example.com',
                'full_name': 'Jane Smith',
                'contact': '9876543210',
                'company': 'Design Studio',
                'address': '456 Oak Ave, Los Angeles, CA',
                'industry': 'Design',
                'password': 'testpass123'
            },
            {
                'email': 'bob.wilson@example.com',
                'full_name': 'Bob Wilson',
                'contact': '5555551234',
                'company': 'Finance Solutions',
                'address': '789 Pine St, Chicago, IL',
                'industry': 'Finance',
                'password': 'testpass123'
            }
        ]

        for user_data in sample_users:
            if not User.objects.filter(email=user_data['email']).exists():
                User.objects.create_user(**user_data)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created user: {user_data["email"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {user_data["email"]}')
                )
