from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import CustomRegisterForm, EmailVerificationForm, LoginForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import EmailVerificationCode
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Представление для регистрации и отправки кода подтвержденния на эл. почту.
def register(request):
    if request.method == 'POST':# Если метод POST, то:
        form = CustomRegisterForm(request.POST)# Заполняем форму данными из запроса.
        if form.is_valid():# Если форма валидна, то:
            user = form.save()# Сохраняем пользователя в БД и помещаем в переменную user.
            code = EmailVerificationCode.generate_code(user)# Генерируем код с помощью метода класса generate_code().
            send_mail(# Отправляем сообщение с кодом.
                subject='Подтверждение почты - Лавка Ирины Плотниковой',
                message=f'Ваш код подтверждения: {code}\nДействителен 10 минут.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            messages.success(request, 'Регистрация прошла успешно! Проверьте email и введите код.')
            return redirect('email_code_confirmation')# Перенаправляем на страницу с формой подстверждения кода.
    else:
        form = CustomRegisterForm()
    return render(request, 'accounts/registration_page.html', {'form': form})

def home_view(request):
    return render(request, 'home_page.html')

# Представление для подтверждения кода email.
def email_code_confirmation_view(request):
    if request.method == 'POST': # Если метод запроса POST:
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']# Достаем код из формы.
            try:
                verification = EmailVerificationCode.objects.select_related('user').get(code=code)
                # Дастаем из БД объект кода подтверждения и подтягиваем данные о пользователе.
                if verification.is_expired():# Проверяем время жизни кода с помощью метода модели.
                    form.add_error('code', 'Код устарел. Запросите новый.')
                else:# Если срок годности не истек, то:
                    user = verification.user
                    user.is_active = True
                    user.save()
                    verification.delete() # Удаляем код подтверждения из БД.
                    login(request, user) # Логиним пользователя
                    return redirect('profile_page') # Перенаправляем нa страницу пользователя.
            except EmailVerificationCode.DoesNotExist:
                form.add_error('code', 'Неверный код.')
    else: # Если метод запроса GET:
        form = EmailVerificationForm()
    return render(request, 'accounts/email_code_confirmation_page.html', {'form': form})

# Представление для повторной отпраки кода подтверждения.
def send_confirmation_code_again(request):
    email = request.POST.get('email') # Достаем email из запроса.
    try:
        user = User.objects.get(email=email, is_active=False)
        # Ищем пользователя с указанным email и неактивированным аккаунтом.
        old_code = EmailVerificationCode.objects.get(user=user) # Достаем из БД старый код подтверждения.
        old_code.delete() # Удаляем его.
        code = EmailVerificationCode.generate_code(user) # Генерируем новый код подтверждения.
        send_mail( # Отправляем его.
            subject='Повторная отправка кода - Лавка Ирины Плотниковой',
            message=f'Ваш код подтверждения: {code}\nДействителен 10 минут.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
        messages.success(request, 'Код отправлен!')
        return redirect('email_code_confirmation')
    except User.DoesNotExist: # Если пользователь с указанным email не найден или аккаунт пользователя
        # уже активирован выводим сообщение. Мы не указываем явно существует ли такой email,
        # что бы защититься от брутфорса и других атак.
        messages.info(request, 'Если этот email зарегистрирован и не подтверждён, вы получите код.')
        return redirect('email_code_confirmation')

# Представление для страницы профиля.
@login_required
def profile_page_view(request):
    return render(request, 'accounts/profile_page.html')

# Представление для авторизации
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)# Находим пользователя через email.
                user = authenticate(request, username=user.username, password=password)
                # Проверяем логин и пароль с помощью функции django authenticate().
            except User.DoesNotExist:
                user = None

            if user is not None:# Если пользователь существует и пароли совпадают:
                login(request, user)# Логиним.
                return redirect('main_page')
            else:
                messages.error(request, 'Неверно введен email или пароль. Попробуйте снова.')
                return redirect('login')
    else:
        form = LoginForm()
        return render(request, 'accounts/login_page.html', {'form': form})

# Представление для выхода из профиля.
def logout_view(request):
    logout(request)
    return redirect('main_page')







