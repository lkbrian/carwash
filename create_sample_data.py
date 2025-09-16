#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from services.models import Service

# Create sample services
services_data = [
    {
        'name': 'Basic Wash',
        'description': 'Exterior wash with soap and rinse',
        'price': 500.00,
        'duration': 30,
    },
    {
        'name': 'Premium Wash',
        'description': 'Exterior wash, interior vacuum, and dashboard cleaning',
        'price': 800.00,
        'duration': 45,
    },
    {
        'name': 'Full Detail',
        'description': 'Complete interior and exterior cleaning with wax',
        'price': 1500.00,
        'duration': 90,
    },
    {
        'name': 'Engine Cleaning',
        'description': 'Professional engine bay cleaning and degreasing',
        'price': 1000.00,
        'duration': 60,
    },
]

for service_data in services_data:
    service, created = Service.objects.get_or_create(
        name=service_data['name'],
        defaults=service_data
    )
    if created:
        print(f"Created service: {service.name}")
    else:
        print(f"Service already exists: {service.name}")

print("Sample data created successfully!")
