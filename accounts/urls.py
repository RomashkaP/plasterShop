from django.urls import path
from .views import register, email_code_confirmation_view, send_confirmation_code_again, \
    profile_page_view, login_view, logout_view, send_code_reset_password_view, confirmation_code_reset_password, \
    reset_password_view



urlpatterns = [
    # Страница регистрации.
    path('registration/', register, name='registration'),
    # Проверка кода подтвеждения эл.почты.
    path('email_code_confirmation/', email_code_confirmation_view, name='email_code_confirmation'),
    # Повторная отправка кода подтверждения эл.почты.
    path('send_conf_code_again/', send_confirmation_code_again, name='send_conf_code_again'),
    # Страница пользователя.
    path('profile_page/', profile_page_view, name='profile_page'),
    # Авторизация.
    path('login/', login_view, name='login'),
    # Выход из профиля.
    path('logout/', logout_view, name='logout'),
    # Отправка кода подтверждения для сброса пароля.
    path('send_code_reset_password/', send_code_reset_password_view, name='send_code_reset_password'),
    # Потверждение кода для сброса пароля.
    path('confirmation_code_reset_password/', confirmation_code_reset_password, name='confirmation_code_reset_password'),
    # Смена пароля.
    path('reset_password/', reset_password_view, name='reset_password'),
]