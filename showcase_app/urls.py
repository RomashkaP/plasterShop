from django.urls import path, include
from .views import *

urlpatterns = [
    # Витрина
    path('showcase_list/', ShowcaseView.as_view(), name='showcase_list'),
    # Отдельный продукт
    path('showcase_list/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
]