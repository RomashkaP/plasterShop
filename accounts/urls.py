from django.urls import path
from .views import register,home_view, email_code_confirmation_view, send_confirmation_code_again


urlpatterns = [
    # Страница регистрации.
    path('registration/', register, name='registration'),
    # Домашняя страница(временно нужно для разработки).
    path('/home/', home_view, name='home'),
    # Проверка кода подтвеждения эл.почты.
    path('email_code_confirmation/', email_code_confirmation_view, name='email_code_confirmation'),
    # Повторная отправка кода подтверждения эл.почты.
    path('send_conf_code_again/', send_confirmation_code_again, name='send_conf_code_again'),
]