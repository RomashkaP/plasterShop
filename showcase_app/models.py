from django.db import models

# Модель товара
class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название товара")  # Название товара
    description = models.TextField(verbose_name="Описание")  # Описание товара
    price = models.PositiveIntegerField(verbose_name="Цена")  # Цена товара

    def __str__(self):
        return self.title
    
    def get_first_image(self):
        try:
            return self.images.all()[0].image.url
        except IndexError:
            return None
        
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

# Модель изображения для товара    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/', verbose_name="Изображение")

    def __str__(self):
        return f"Изображение для: {self.product.title}"
    
    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

# Модель характеристик для товара
class ProductCharacteristics(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="characteristics")
    height = models.IntegerField(verbose_name="Высота в сантиметрах")  # Высота
    width = models.IntegerField(verbose_name="Ширина в сантиметрах")  # Ширина
    weight = models.IntegerField(verbose_name="Вес в граммах")  # Вес
    material = models.CharField(max_length=255, verbose_name="Материал")

    def __str__(self):
        return f"Характеристики для: {self.product.title}"
    
    class Meta:
        verbose_name = "Характеристики товара"
        verbose_name_plural = "Характеристики товара"

# Модель категории для товара
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название категории")
    products = models.ManyToManyField(Product, related_name="categories", blank=True)

    def __str__(self):
            return self.title
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
