from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from users.forms import CustomUserCreationForm, EmployeeRegistrationForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from services.models import Service
from bookings.models import Booking
from payments.models import Payment
from users.models import Profile
import uuid

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def services_view(request):
    services = Service.objects.filter(is_active=True)
    pending_payment = None
    
    if request.user.is_authenticated:
        # Check for any pending payments
        pending_payment = Booking.objects.filter(
            customer=request.user, 
            status='pending'
        ).first()
    
    return render(request, 'services.html', {
        'services': services,
        'pending_payment': pending_payment
    })

@login_required
def dashboard_view(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'bookings': bookings})

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)
    
    if request.method == 'POST':
        booking = Booking.objects.create(
            customer=request.user,
            service=service,
            booking_date=request.POST['booking_date'],
            booking_time=request.POST['booking_time'],
            car_model=request.POST['car_model'],
            car_plate=request.POST['car_plate'],
            notes=request.POST.get('notes', '')
        )
        
        Payment.objects.create(
            booking=booking,
            amount=service.price,
            transaction_id=str(uuid.uuid4())
        )
        
        return redirect('payment', booking_id=booking.id)
    
    return render(request, 'booking_form.html', {'service': service})

@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    payment = get_object_or_404(Payment, booking=booking)
    return render(request, 'payment.html', {'booking': booking, 'payment': payment})

@login_required
def process_payment(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
        payment = get_object_or_404(Payment, booking=booking)
        
        payment_method = request.POST.get('payment_method', 'mpesa')
        payment.payment_method = payment_method
        payment.status = 'completed'
        payment.completed_at = timezone.now()
        payment.save()
        
        booking.status = 'confirmed'
        booking.save()
        
        # Send confirmation email
        try:
            from notifications.utils import send_booking_confirmation
            send_booking_confirmation(booking)
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        messages.success(request, 'Payment successful! Booking confirmed. Check your email for confirmation.')
        return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
    
    return JsonResponse({'success': False})

@require_http_methods(["GET"])
def check_username(request):
    username = request.GET.get('username', '').strip()
    if not username:
        return JsonResponse({'available': True})
    
    exists = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({'available': not exists})

@require_http_methods(["GET"])
def check_email(request):
    email = request.GET.get('email', '').strip()
    if not email:
        return JsonResponse({'available': True})
    
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'available': not exists})

def logout_view(request):
    logout(request)
    return redirect('login')

def employee_register_view(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Employee registration submitted! Please wait for admin approval.')
            return redirect('login')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'registration/employee_register.html', {'form': form})

@login_required
def employee_dashboard(request):
    if not request.user.profile.is_employee():
        messages.error(request, 'Access denied. Employee account required.')
        return redirect('dashboard')
    
    if not request.user.profile.is_approved:
        messages.warning(request, 'Your account is pending approval.')
        return redirect('home')
    
    # Get bookings for employee
    assigned_bookings = Booking.objects.filter(assigned_employee=request.user)
    available_bookings = Booking.objects.filter(status='confirmed', assigned_employee=None)
    
    return render(request, 'employee_dashboard.html', {
        'assigned_bookings': assigned_bookings,
        'available_bookings': available_bookings
    })

@login_required
def claim_booking(request, booking_id):
    if not request.user.profile.is_employee() or not request.user.profile.is_approved:
        return JsonResponse({'success': False, 'error': 'Access denied'})
    
    booking = get_object_or_404(Booking, id=booking_id, status='confirmed', assigned_employee=None)
    booking.assigned_employee = request.user
    booking.status = 'assigned'
    booking.save()
    
    messages.success(request, f'Booking #{booking.ticket_number} claimed successfully!')
    return JsonResponse({'success': True})

@login_required
def update_booking_status(request, booking_id):
    if not request.user.profile.is_employee():
        return JsonResponse({'success': False, 'error': 'Access denied'})
    
    booking = get_object_or_404(Booking, id=booking_id, assigned_employee=request.user)
    new_status = request.POST.get('status')
    
    if new_status in ['in_progress', 'completed']:
        booking.status = new_status
        if new_status == 'in_progress' and not booking.work_started_at:
            from django.utils import timezone
            booking.work_started_at = timezone.now()
        elif new_status == 'completed':
            from django.utils import timezone
            booking.work_completed_at = timezone.now()
        
        booking.save()
        
        # Send notification email to customer
        try:
            from notifications.utils import send_status_update
            send_status_update(booking)
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        messages.success(request, f'Booking #{booking.ticket_number} status updated to {new_status}!')
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid status'})
