from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random

# Модель для хранения кодов подтверждения при регистрации.
class EmailVerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    # Метод для проверки срока годности кода.
    def is_expired(self, minutes=10):
        return (timezone.now() - self.created_at).total_seconds() > minutes * 60

    # Метод класса (что бы не создавать экземпляр класса) для генерации кода.
    @classmethod
    def generate_code(cls, user):
        cls.objects.filter(user=user).delete # Удаляем старый код.
        code = str(random.randint(100000, 999999))
        obj = cls.objects.create(user=user, code=code)
        return code

