from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomRegisterForm


def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = CustomRegisterForm()
    return render(request, 'accounts/registration_page.html', {'form': form})

def home_view(request):
    return render(request, 'home_page.html')


