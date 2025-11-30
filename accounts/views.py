from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import CustomRegisterForm, EmailVerificationForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import EmailVerificationCode


def register(request):# Представление для регистрации.
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            code = EmailVerificationCode.generate_code(user)
            send_mail(
                subject='Подтверждение почты - Лавка Ирины Плотниковой',
                message=f'Ваш код подтверждения: {code}\nДействителен 10 минут.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            messages.success(request, 'Регистрация прошла успешно! Проверьте email и введите код.')
            return redirect('email_code_confirmation')
    else:
        form = CustomRegisterForm()
    return render(request, 'accounts/registration_page.html', {'form': form})

def home_view(request):
    return render(request, 'home_page.html')

def email_code_confirmation_view(request):# Представление для подтверждения кода email.
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                verification = EmailVerificationCode.objects.select_related('user').get(code=code)
                if verification.is_expired():
                    form.add_error('code', 'Код устарел. Запросите новый.')
                else:
                    user = verification.user
                    user.is_active = True
                    user.save()
                    verification.delete()
                    return redirect('home')
            except EmailVerificationCode.DoesNotExists:
                form.add_error('code', 'Неверный код.')
    else:
        form = EmailVerificationForm()
    return render(request, 'accounts/email_code_confirmation_page.html', {'form': form})




