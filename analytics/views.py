from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from bookings.models import Booking, Review
from services.models import Service
from payments.models import Payment
from users.models import Profile
import json

@login_required
def analytics_dashboard(request):
    if not request.user.profile.is_employee:
        return redirect('dashboard')
    
    # Date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Revenue Analytics
    total_revenue = Payment.objects.filter(
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    monthly_revenue = Payment.objects.filter(
        status='completed',
        created_at__date__gte=month_ago
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    weekly_revenue = Payment.objects.filter(
        status='completed',
        created_at__date__gte=week_ago
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Booking Analytics
    total_bookings = Booking.objects.count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    
    # Service Popularity
    service_stats = Service.objects.annotate(
        booking_count=Count('booking'),
        total_revenue=Sum('booking__payment__amount', filter=Q(booking__payment__status='completed'))
    ).order_by('-booking_count')
    
    # Customer Retention (repeat customers)
    repeat_customers = Booking.objects.values('customer').annotate(
        booking_count=Count('id')
    ).filter(booking_count__gt=1).count()
    
    total_customers = Booking.objects.values('customer').distinct().count()
    retention_rate = (repeat_customers / total_customers * 100) if total_customers > 0 else 0
    
    # Average Rating
    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
    
    # Recent Reviews
    recent_reviews = Review.objects.select_related('booking__customer', 'booking__service').order_by('-created_at')[:5]
    
    context = {
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'weekly_revenue': weekly_revenue,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'pending_bookings': pending_bookings,
        'service_stats': service_stats,
        'retention_rate': round(retention_rate, 1),
        'avg_rating': round(avg_rating, 1),
        'recent_reviews': recent_reviews,
    }
    
    return render(request, 'analytics/dashboard.html', context)
