from django.contrib import admin
from .models.orders import Order, OrderItem
from .models.payments import Payment

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'boutique', 'status', 'payment_status', 'total_amount', 'created_at')
    search_fields = ('order_number', 'customer__user__username', 'boutique__name')
    list_filter = ('status', 'payment_status', 'created_at', 'updated_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'status', 'created_at')
    search_fields = ('order__order_number', 'product__name')
    list_filter = ('status', 'created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'boutique', 'amount', 'currency', 'payment_method', 'status', 'paid_at', 'created_at')
    search_fields = ('order__order_number', 'customer__user__username', 'boutique__name')
    list_filter = ('payment_method', 'status', 'created_at', 'updated_at')
