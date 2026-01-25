from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

# Представление для отображения витрины
class ShowcaseView(ListView):
    model = Product
    template_name = 'showcase_app/showcase_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()    

# Представление для отображения отдельного товара
class ProductDetailView(DetailView):
    model = Product
    template_name = 'showcase_app/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.select_related('characteristics').prefetch_related('images').all()