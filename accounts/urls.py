from django.urls import path
from .views import register,home_view, email_code_confirmation_view, send_confirmation_code_again, \
    profile_page_view, login_view, logout_view



urlpatterns = [
    # Страница регистрации.
    path('registration/', register, name='registration'),
    # Проверка кода подтвеждения эл.почты.
    path('email_code_confirmation/', email_code_confirmation_view, name='email_code_confirmation'),
    # Повторная отправка кода подтверждения эл.почты.
    path('send_conf_code_again/', send_confirmation_code_again, name='send_conf_code_again'),
    # Страница пользователя.
    path('profile_page/', profile_page_view, name='profile_page'),
    # Авторизация
    path('login/', login_view, name='login'),
    # Выход из профиля
    path('logout/', logout_view, name='logout'),
]