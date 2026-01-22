from django.db import models
from django.contrib.auth.models import User

# Модель поста
class Post(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    # Счетчик просмотров поста
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

# Модель комментария
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    time_in = models.DateTimeField(auto_now_add=True)
