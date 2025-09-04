# filepath: ~/nzi-market/back_boutiques/orders/urls.py
from django.urls import path
from .views.orders import OrderListView, OrderDetailView
from .views.payments import PaymentListView, PaymentDetailView

urlpatterns = [
    path('api/', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/api/', OrderDetailView.as_view(), name='order-detail'),
    path('payments/api/', PaymentListView.as_view(), name='payment-list'),
    path('payments/<int:pk>/api/', PaymentDetailView.as_view(), name='payment-detail'),
]
# Note: Ensure that the views and serializers are correctly implemented in the respective files.
# This file defines the URL patterns for the order-related and payment-related API endpoints.