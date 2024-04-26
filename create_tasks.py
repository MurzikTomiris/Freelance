import os
import django
from faker import Faker
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from freelace.models import Service

def create_services(n):
    fake = Faker()

    for _ in range(n):
        Service.objects.create(
            executor = executor
        )

if __name__ == '__main__':
    print('Creating persons...')
    create_persons(100)  # Генерируем 100 записей
    print('Done!')
