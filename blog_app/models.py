from django.db import models
from django.contrib.auth.models import User

# Модель поста
class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    time_in = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name="Изображение")
    # Счетчик просмотров поста
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Запись блога"
        verbose_name_plural = "Записи блога"

# Модель комментария
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст комметария")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    time_in = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
