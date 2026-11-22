from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Booking, ContactMessage


class BookingForm(forms.ModelForm):
    """Форма создания/редактирования брони."""

    class Meta:
        model = Booking
        # user заполняем во view, поэтому его нет в fields
        fields = ['table', 'date', 'time', 'guests_count']
        widgets = {
            'table': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'guests_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
        }
        labels = {
            'table': 'Столик',
            'date': 'Дата',
            'time': 'Время',
            'guests_count': 'Количество гостей',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # в выпадающем списке — только активные столики
        self.fields['table'].queryset = self.fields['table'].queryset.filter(is_active=True)

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.localdate():
            raise forms.ValidationError('Нельзя бронировать на прошедшую дату.')
        return date

    def clean(self):
        cleaned = super().clean()
        table = cleaned.get('table')
        guests = cleaned.get('guests_count')
        date = cleaned.get('date')
        time = cleaned.get('time')

        # гостей не больше, чем мест за столом
        if table and guests and guests > table.capacity:
            self.add_error('guests_count', f'За этим столиком только {table.capacity} мест.')

        # столик не занят на это же время
        if table and date and time:
            conflict = Booking.objects.filter(
                table=table, date=date, time=time
            ).exclude(status='cancelled')

            # 🔥 при редактировании исключаем текущую бронь из проверки
            if self.instance and self.instance.pk:
                conflict = conflict.exclude(pk=self.instance.pk)

            if conflict.exists():
                self.add_error('time', 'Этот столик уже забронирован на это время.')

        return cleaned


class ContactForm(forms.ModelForm):
    """Форма обратной связи."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                             'placeholder': 'Ваше сообщение'}),
        }


class RegisterForm(UserCreationForm):
    """Форма регистрации: UserCreationForm + email + Bootstrap."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
        label='Email'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Повторите пароль'})
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повтор пароля'