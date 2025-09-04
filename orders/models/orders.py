from django.db import models
from django.contrib.auth.models import User
from accounts.models.members import MemberProfile
from accounts.models.boutiques import BoutiqueProfile
from products.models import Product
from quotes.models import Quote, QuoteItem


# Create your models here.


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]

    customer = models.ForeignKey(MemberProfile, related_name='orders', on_delete=models.CASCADE)
    boutique = models.ForeignKey(BoutiqueProfile, related_name='orders', on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=32, unique=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_address = models.CharField(max_length=512)
    billing_address = models.CharField(max_length=512, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number} by {self.customer}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quote_item = models.ForeignKey(QuoteItem, related_name='order_items', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('fulfilled', 'Fulfilled'),
            ('cancelled', 'Cancelled'),
            ('returned', 'Returned'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OrderItem {self.product} x{self.quantity} for Order {self.order.order_number}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'