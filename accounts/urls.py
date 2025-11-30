from django.urls import path
from .views import register,home_view


urlpatterns = [
    path('registration/', register, name='registration'),
    path('home/', home_view, name='home'),
]