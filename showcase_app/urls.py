from django.urls import path, include
from .views import *

urlpatterns = [
    # Витрина
    path('', ShowcaseView.as_view(), name='showcase_list'),
    # Отдельный продукт
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]