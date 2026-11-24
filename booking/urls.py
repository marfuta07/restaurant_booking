from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('booking/', views.booking_view, name='booking'),
    path('booking/<int:pk>/success/', views.booking_success_view, name='booking_success'),  # 🆕
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('booking/<int:pk>/edit/', views.booking_edit_view, name='booking_edit'),
    path('booking/<int:pk>/cancel/', views.booking_cancel_view, name='booking_cancel'),
    path('register/', views.register_view, name='register'),
    path('contacts/', views.contacts_view, name='contacts'),
]
