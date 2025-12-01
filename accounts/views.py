from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import CustomRegisterForm, EmailVerificationForm, SendVerificationcodeAgainForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import EmailVerificationCode
from django.contrib.auth.models import User

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
    if request.method == 'POST':
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
                    return redirect('home') # Перенаправляем на домашнюю страницу.
            except EmailVerificationCode.DoesNotExists:
                form.add_error('code', 'Неверный код.')
    else:
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







