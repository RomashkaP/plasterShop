from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('post_list/', PostListView.as_view(), name='post_list'),
]
