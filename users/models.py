from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('washer', 'Washer'),
        ('supervisor', 'Supervisor'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    is_approved = models.BooleanField(default=True)  # False for employees pending approval
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def is_employee(self):
        return self.role in ['washer', 'supervisor', 'admin']
