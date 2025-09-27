"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('services/', views.services_view, name='services'),
    path('register_type/', views.register_type_view, name='register_type'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment'),
    path('process-payment/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('api/check-username/', views.check_username, name='check_username'),
    path('api/check-email/', views.check_email, name='check_email'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
    path('employee/register/', views.employee_register_view, name='employee_register'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/claim/<int:booking_id>/', views.claim_booking, name='claim_booking'),
    path('employee/complete/<int:booking_id>/', views.complete_booking, name='complete_booking'),
    path('employee/update-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
    
    # Supervisor URLs
    path('supervisor/dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('supervisor/approve/<int:booking_id>/', views.approve_job, name='approve_job'),
    path('supervisor/reject/<int:booking_id>/', views.reject_job, name='reject_job'),
    path('supervisor/assign/<int:booking_id>/', views.assign_job, name='assign_job'),
    
    # Admin Dashboard URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/employees/', views.manage_employees, name='manage_employees'),
    path('admin-dashboard/employees/approve/<int:user_id>/', views.approve_employee, name='approve_employee'),
    path('admin-dashboard/employees/reject/<int:user_id>/', views.reject_employee, name='reject_employee'),
    path('admin-dashboard/services/', views.manage_services, name='manage_services'),
    path('admin-dashboard/services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    path('admin-dashboard/services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('admin-dashboard/services/toggle/<int:service_id>/', views.toggle_service, name='toggle_service'),
    
    # Analytics and Review URLs
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('review/<int:booking_id>/', views.add_review, name='add_review'),
]
