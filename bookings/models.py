from django.db import models
from django.contrib.auth.models import User
from services.models import Service
import uuid

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('assigned', 'Assigned to Employee'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    ticket_number = models.CharField(max_length=10, unique=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_bookings')
    assigned_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    car_model = models.CharField(max_length=100)
    car_plate = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    work_started_at = models.DateTimeField(null=True, blank=True)
    work_completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"CW{str(uuid.uuid4().int)[:6]}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"#{self.ticket_number} - {self.customer.username} - {self.service.name}"
    
    class Meta:
        ordering = ['-created_at']
