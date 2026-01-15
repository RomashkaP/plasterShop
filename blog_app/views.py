from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView 
from .models import Post

# Дженерик для просмотра всех статей
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = '-time_in'



