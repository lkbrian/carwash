import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from services.models import Service

# Clear existing services
Service.objects.all().delete()

services_data = [
    # Exterior Services
    {
        'name': 'Exterior Washing',
        'description': 'Complete exterior car wash with premium waterless cleaning products',
        'price': 800,
        'duration': 45
    },
    {
        'name': 'Drive-Thru Wash',
        'description': 'Quick and convenient drive-through car wash service',
        'price': 500,
        'duration': 15
    },
    {
        'name': 'Wheel Cleaning',
        'description': 'Professional wheel and rim cleaning service',
        'price': 300,
        'duration': 20
    },
    {
        'name': 'Hand Car Wash',
        'description': 'Premium hand wash service with attention to detail',
        'price': 1000,
        'duration': 60
    },
    
    # Interior Services
    {
        'name': 'Interior Detailing',
        'description': 'Complete interior cleaning and detailing service',
        'price': 1200,
        'duration': 90
    },
    {
        'name': 'Interior Cleaning',
        'description': 'Basic interior vacuum and wipe down service',
        'price': 600,
        'duration': 30
    },
    
    # Detailing Services
    {
        'name': 'Glass Polishing',
        'description': 'Professional glass cleaning and polishing for crystal clear visibility',
        'price': 400,
        'duration': 25
    },
    {
        'name': 'Crystal Shine',
        'description': 'Premium polishing service for showroom-quality shine',
        'price': 1500,
        'duration': 120
    },
    
    # Engine Services
    {
        'name': 'Engine Cleaning',
        'description': 'Professional engine bay cleaning and degreasing',
        'price': 800,
        'duration': 45
    },
    {
        'name': 'Engine Service',
        'description': 'Complete engine maintenance and cleaning service',
        'price': 2000,
        'duration': 180
    },
    
    # Diagnostic Services
    {
        'name': 'Diagnostic Tests',
        'description': 'Comprehensive vehicle diagnostic and inspection service',
        'price': 1000,
        'duration': 60
    },
    
    # Premium Package
    {
        'name': 'Premium Waterless Package',
        'description': 'Complete waterless cleaning service at your doorstep - includes exterior wash, interior cleaning, and glass polishing',
        'price': 2500,
        'duration': 150
    }
]

for service_data in services_data:
    service = Service.objects.create(**service_data)
    print(f"Created: {service.name} - KES {service.price}")

print(f"\nTotal services created: {Service.objects.count()}")
