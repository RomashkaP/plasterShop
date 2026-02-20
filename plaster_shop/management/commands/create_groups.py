from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Команда для создания групп пользователей - Простой пользователь и Администратор
class Command(BaseCommand):
    help = 'Создает группы пользователей'

    def handle(self, *args, **options):
  
        # Находим или создаем группу admin    
        admin_group, created = Group.objects.get_or_create(name='admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "admin" создана'))

        # Присваем группе админ все права
        all_perms = Permission.objects.all()
        for perm in all_perms:
            admin_group.permissions.add(perm)
        
        self.stdout.write(self.style.SUCCESS('Группы успешно созданы и настроены'))
