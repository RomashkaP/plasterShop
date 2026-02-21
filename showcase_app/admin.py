from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

admin.site.register(ProductImage)
admin.site.register(ProductCharacteristics)
admin.site.register(Category)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image',)

class ProductCharacteristicsInline(admin.StackedInline):
    model = ProductCharacteristics
    can_delete = False
    fields = ('height', 'width', 'weight', 'material')

class ProductCategoryInline(admin.TabularInline):
    model = Product.categories.through
    extra = 1
    verbose_name = "Категория"
    verbose_name_plural = "Категории"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'get_first_category', 'get_first_image_preview')
    list_filter = ('categories',)
    search_fields = ('title', 'description')
    inlines = [ProductCharacteristicsInline, ProductImageInline, ProductCategoryInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'price')
        }),
    )

    def get_first_category(self, obj):
        return ", ".join([cat.title for cat in obj.categories.all()[:3]])
    get_first_category.short_description = 'Категории'

    def get_first_image_preview(self, obj):
        first_img = obj.get_first_image()
        if first_img:
            return mark_safe(f'<img src="{first_img}" style="height: 100px; object-fit: cover;">')
        return 'Нет изображений'
    get_first_image_preview.short_description = 'Изображение'
    get_first_image_preview.allow_tags = True

admin.site.unregister(ProductImage)
admin.site.unregister(ProductCharacteristics)

# === Скрытие моделей python-social-auth из админки ===
from django.apps import apps

# Попробуем найти приложение social_django и отключить его модели
try:
    from social_django.models import UserSocialAuth, Nonce, Association, Code, Partial
    from django.contrib import admin

    # Убираем каждую модель из админки
    admin.site.unregister(UserSocialAuth)
    admin.site.unregister(Nonce)
    admin.site.unregister(Association)
    admin.site.unregister(Code)
    admin.site.unregister(Partial)
except ImportError:
    # social_django не установлен
    pass
except admin.sites.NotRegistered:
    # Модель уже не зарегистрирована — всё ок
    pass