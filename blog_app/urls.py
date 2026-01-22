from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # Страница с постами
    path('post_list/', PostListView.as_view(), name='post_list'),
    # Отдельный пост
    path('post_list/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    # Создание комментария
    path('post_list/<int:pk>/comment/', create_comment_view, name='comment_create'),
]
