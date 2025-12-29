from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import CustomRegisterForm, EmailVerificationForm, LoginForm, EmailInputReplacePasswordForm,\
    ResetPasswordForm
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


# Представление для повторной отправки кода подтверждения.
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
                # На будущее - лучше сразу использовать кастомную модель пользователя с email как уникальным полем
                # и USERNAME_FIELD = 'email'.
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
        password_replace_form = EmailInputReplacePasswordForm()
        return render(request, 'accounts/login_page.html', {'form': form, 'prform': password_replace_form})


# Представление для выхода из профиля.
def logout_view(request):
    logout(request)
    return redirect('main_page')


# Представление отправки кода для смены пароля.
def send_code_reset_password_view(request):
    if request.method == 'POST':
        form = EmailInputReplacePasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']# Достаем email из формы.
            try:
                user = User.objects.get(email=email)# Достаем пользователя по email.
            except User.DoesNotExist:
                user = None
            if user:# Если пользователь существует:
                old_code = EmailVerificationCode.objects.filter(user=user).first()
                # Достаем из БД старый код подтверждения.
                if old_code:
                    old_code.delete()
                code = EmailVerificationCode.generate_code(user)# Генерируем новый код подтверждения.
                send_mail(
                    subject='Смена пароля - Лавка Ирины Плотниковой',
                    message=f'Ваш код подтверждения: {code}\nДействителен 10 минут.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False
                )
                messages.info(request, 'Если этот email зарегистрирован, вы получите код.')
                return redirect('confirmation_code_reset_password')
            else:
                messages.info(request, 'Если этот email зарегистрирован, вы получите код.')
                return redirect('confirmation_code_reset_password')
    else:
        form = EmailInputReplacePasswordForm()
        return render(request, 'accounts/password_reset_page.html', {'form': form})


# Представление обработки кода подтверждения смены пароля.
def confirmation_code_reset_password(request):
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']# Достаем код из формы.
            try:
                verification = EmailVerificationCode.objects.select_related('user').get(code=code)
                # Достаем код подтверждения и данные пользователя из БД. 
                if verification.is_expired():# Если время действия кода истекло:
                    messages.error(request, 'Время действия кода истекло. Повторите попытку.')
                    return redirect('login')
                
                request.session['reset_user_id'] = verification.user.id
                # Сохраняем id пользователя в сессии.
                request.session.set_expiry(600) # Устанавливаем время жизни сессии 10 минут.
                verification.delete()# Удаляем код подтверждения.
                return redirect('reset_password')
            
            except EmailVerificationCode.DoesNotExist: # Если код не найден:
                messages.error(request, 'Неверный код.')
                return redirect('confirmation_code_reset_password')
    else:
        form = EmailVerificationForm()
        return render(request, 'accounts/email_code_reset_password_page.html', {'form': form})
    

# Представление для смены пароля.
def reset_password_view(request):
    user_id = request.session.get('reset_user_id') # Достаем id пользователя из сессии.
    if not user_id:
        messages.error(request, 'Доступ запрещён. Повторите процесс заново.')
        return redirect('login')
    try:
        user = User.objects.get(id=user_id) # Находим пользователя по id.
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден.')
        return redirect('login')
    
    if request.method == 'POST':
        form = ResetPasswordForm(user, request.POST) # Передаем пользователя в форму.
        if form.is_valid():
            form.save() # Сохраняем новый пароль. Django хэширует пароль через user.set_password(raw_password).
            # Вызывает user.save().
            del request.session['reset_user_id'] # Удаляем id пользователя из сессии.
            messages.success(request, 'Пароль успешно изменен. Войдите с новым паролем.')
            return redirect('login')
    else:
        form = ResetPasswordForm(user)
        return render(request, 'accounts/reset_password_page.html', {'form': form})
                





