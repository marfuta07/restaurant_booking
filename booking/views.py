from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Service, TeamMember, Table, Booking
from .forms import BookingForm, ContactForm, RegisterForm


def home(request):
    """Главная: услуги, команда + форма обратной связи (по ТЗ)."""
    services = Service.objects.all()
    team = TeamMember.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение отправлено! Мы ответим в ближайшее время.')
            return redirect('booking:home')
    else:
        form = ContactForm()

    return render(request, 'booking/home.html', {
        'services': services,
        'team': team,
        'form': form,
    })


def about_view(request):
    """Страница «О ресторане» — команда. (История/миссия — в шаблоне, День 2.)"""
    team = TeamMember.objects.all()
    return render(request, 'booking/about.html', {'team': team})


@login_required
def booking_view(request):
    """Создание брони. После успеха — редирект на страницу подтверждения."""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Спасибо! Заявка принята.')
            return redirect('booking:booking_success', pk=booking.pk)  # 🔥 на success-страницу
    else:
        form = BookingForm()
    return render(request, 'booking/booking.html', {'form': form})

@login_required
def booking_success_view(request, pk):
    """Страница подтверждения брони."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'booking/booking_success.html', {'booking': booking})

@login_required
def my_bookings_view(request):
    """История броней текущего пользователя."""
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required
def booking_edit_view(request, pk):
    """Редактирование своей брони. Чужую — 404 (IDOR-защита)."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Бронирование обновлено.')
            return redirect('booking:my_bookings')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking/booking.html', {'form': form, 'edit_mode': True})


@login_required
def booking_cancel_view(request, pk):
    """Отмена своей брони (только через POST)."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Бронирование отменено.')
        return redirect('booking:my_bookings')
    return render(request, 'booking/booking_cancel.html', {'booking': booking})


def register_view(request):
    """Регистрация пользователя с автологином."""
    if request.user.is_authenticated:
        return redirect('booking:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('booking:home')
    else:
        form = RegisterForm()
    return render(request, 'booking/register.html', {'form': form})


def contacts_view(request):
    """Страница контактов с формой обратной связи."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение отправлено! Мы ответим в ближайшее время.')
            return redirect('booking:contacts')
    else:
        form = ContactForm()
    return render(request, 'booking/contacts.html', {'form': form})