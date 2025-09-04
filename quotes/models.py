from django.db import models
from django.contrib.auth.models import User
from accounts.models.members import MemberProfile
from accounts.models.boutiques import BoutiqueProfile
from products.models import Product

# Create your models here.

class Quote(models.Model):
    customer = models.ForeignKey(MemberProfile, related_name='quotes', on_delete=models.CASCADE)
    boutique = models.ForeignKey(BoutiqueProfile, related_name='quotes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('sent', 'Sent'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='draft')

    def __str__(self):
        return f"Quote {self.id} for {self.customer}"
    
    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ['-created_at']
    

class QuoteItem(models.Model):
    quote = models.ForeignKey(Quote, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='quote_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"QuoteItem for {self.product} in {self.quote}"
    
    class Meta:
        verbose_name = "Quote Item"
        verbose_name_plural = "Quotes Items"
        ordering = ['-created_at']
        unique_together = ('quote', 'product') 
    
