from django.db import models
from django.contrib.auth.models import User
from bookings.models import Booking
from services.models import Service
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta

class AnalyticsReport(models.Model):
    REPORT_TYPES = [
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
    ]
    
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    date = models.DateField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_bookings = models.IntegerField(default=0)
    completed_bookings = models.IntegerField(default=0)
    cancelled_bookings = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['report_type', 'date']
    
    def __str__(self):
        return f"{self.report_type.title()} Report - {self.date}"

class ServiceAnalytics(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    bookings_count = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_rating = models.FloatField(default=0)
    
    class Meta:
        unique_together = ['service', 'date']
    
    def __str__(self):
        return f"{self.service.name} - {self.date}"
