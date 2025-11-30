from django.urls import path
from .views import register,home_view, email_code_confirmation_view


urlpatterns = [
    path('registration/', register, name='registration'),
    path('/home/', home_view, name='home'),
    path('email_code_confirmation/', email_code_confirmation_view, name='email_code_confirmation'),
]