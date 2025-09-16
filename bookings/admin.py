from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'service', 'booking_date', 'booking_time', 'status', 'created_at']
    list_filter = ['status', 'booking_date', 'created_at']
    search_fields = ['customer__username', 'service__name', 'car_plate']
    date_hierarchy = 'booking_date'
