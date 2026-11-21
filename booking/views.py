from django.shortcuts import render
from .models import Service, TeamMember, Table

def home(request):
    # Берем все услуги из базы данных
    services = Service.objects.all()
    # Передаем их в шаблон
    return render(request, 'booking/home.html', {'services': services})