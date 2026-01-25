from django.db import models

# Модель товара
class Product(models.Model):
    title = models.CharField(max_length=255)  # Название товара
    description = models.TextField()  # Описание товара
    price = models.PositiveIntegerField()  # Цена товара

    def __str__(self):
        return self.title
    
    def get_first_image(self):
        try:
            return self.images.all()[0].image.url
        except IndexError:
            return None

# Модель изображения для товара    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Изображение для: {self.product.title}"

# Модель характеристик для товара
class ProductCharacteristics(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="characteristics")
    height = models.IntegerField()  # Высота
    width = models.IntegerField()  # Ширина
    weight = models.IntegerField()  # Вес
    material = models.CharField(max_length=255)

    def __str__(self):
        return f"Характеристики для: {self.product.title}"

# Модель категории для товара
class Category(models.Model):
    title = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name="categories", blank=True)

    def __str__(self):
            return self.title
    
