from django.urls import path
from products.views import ProductView, ProductCategoryView

urlpatterns = [
    path('categories/api/', ProductCategoryView.as_view(), name='category-list'),
    path('categories/<int:pk>/api/', ProductCategoryView.as_view(), name='category-details'),
    path('api/', ProductView.as_view(), name='product-list'),
    path('<int:pk>/api/', ProductView.as_view(), name='product-details'),
]