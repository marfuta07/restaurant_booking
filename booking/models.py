from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    icon = models.CharField(max_length=50, verbose_name="Иконка (класс Bootstrap)", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class TeamMember(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    role = models.CharField(max_length=100, verbose_name="Должность")
    photo = models.ImageField(upload_to='team/', verbose_name="Фото", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Член команды"
        verbose_name_plural = "Команда"


class Table(models.Model):
    number = models.IntegerField(unique=True, verbose_name="Номер столика")
    capacity = models.IntegerField(verbose_name="Вместимость (чел.)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"Столик {self.number} (до {self.capacity} чел.)"

    class Meta:
        verbose_name = "Столик"
        verbose_name_plural = "Столики"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name="Столик")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    guests_count = models.IntegerField(verbose_name="Количество гостей")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def __str__(self):
        return f"Бронь {self.user.username} - Столик {self.table.number} на {self.date} {self.time}"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"Сообщение от {self.name}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
