from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

# Форма для регистрации пользователя.
class CustomRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=35, label='Имя')
    last_name = forms.CharField(max_length=35, label='Фамилия')
    username = forms.CharField(max_length=50, label='Псевдоним')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        min_length=10
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким псевдонимом уже зарегистрирован.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        try:
            validate_password(password) # Функция валидации пароля django.
        except ValidationError as e:
            raise ValidationError(e.messages)
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают.')
        return password2

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            is_active=False # Создаем со значением False для реализации методов подтверждения данных пользователя.
        )
        return user

# Форма для кода подтверждения.
class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        label='Код подтверждения',
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'placeholder': '1234567'})
    )

# Форма для логина.
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        min_length=10
    )



