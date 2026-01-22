from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView 
from django.db.models import Count
from .models import *

# Дженерик для просмотра всех статей
class PostListView(ListView):
    model = Post
    template_name = 'blog_app/post_list.html'
    context_object_name = 'posts'
    ordering = '-time_in'

    def get_queryset(self): # Переопределение метода get_queryset для подсчета комментариев
        return Post.objects.annotate(  # Функция annotate позволяет добавить поле в модель
            comments_count=Count('comments')
        ).order_by('-time_in')

# Дженерик для просмотра одной статьи
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'
    context_object_name = 'post'

    # Переопределение метода get для увеличения количества просмотров
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        session_key = f'viewed_post_{self.object.id}'

        if not request.session.get(session_key):
           self.object.views += 1
           self.object.save(update_fields=['views'])
           request.session[session_key] = True
        
        return super().get(request, *args, **kwargs)
    
    # Переопределение метода get_context_data для передачи комментариев в шаблон
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-time_in')
        return context

# Представление для создания комментария
def create_comment_view(request, pk):
    user = request.user
    text = request.POST.get('comment_text')
    post = Post.objects.get(pk=pk)
    comment_object = Comment.objects.create(
            user=user,
            text=text,
            post=post
    )
    return redirect('post_detail', pk=pk)


