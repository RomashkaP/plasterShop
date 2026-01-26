from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

# Представление для отображения витрины
class ShowcaseView(ListView):
    model = Product
    template_name = 'showcase_app/showcase_list.html'
    context_object_name = 'products'

    # Переопределение метода get_queryset()
    def get_queryset(self):
        queryset =  Product.objects.prefetch_related('images')

        # Фильтрация по категории
        category_id = self.request.GET.get('category')
        if category_id:
            if Category.objects.filter(id=category_id).exists():
                queryset = queryset.filter(categories__id=category_id)

        # Сортировка по цене
        sort = self.request.GET.get('sort')
        allowed_sort = ['price_inc', 'price_dec']
        if sort in allowed_sort:
            if sort == 'price_inc':
                queryset = queryset.order_by('price') # Сортировка по возрастанию
            elif sort == 'price_dec':
                queryset = queryset.order_by('-price') # Сортировка по убыванию
        else:
            queryset = queryset.order_by('-id') # Сортировка по умолчанию

        return queryset
    
    # Переопределение метода get_context_data() для передачи категорий
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() # Получение всех категорий
        context['current_category'] = self.request.GET.get('category') # Получение текущей категории
        context['current_sort'] = self.request.GET.get('sort') # Получение текущего типа сортировки
        return context

# Представление для отображения отдельного товара
class ProductDetailView(DetailView):
    model = Product
    template_name = 'showcase_app/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.select_related('characteristics').prefetch_related('images').all()