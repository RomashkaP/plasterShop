from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import CustomRegisterForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings


def register(request):# Представление для регистрации.
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()



            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('email_code_confirmation')
    else:
        form = CustomRegisterForm()
    return render(request, 'accounts/registration_page.html', {'form': form})

def home_view(request):
    return render(request, 'home_page.html')

def email_code_confirmation_view(request):# Представление для подтверждения кода email.
    return render(request, 'accounts/email_code_confirmation_page.html')




