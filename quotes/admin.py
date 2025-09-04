from django.contrib import admin
from .models import Quote, QuoteItem

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'boutique', 'status', 'created_at', 'updated_at')
    search_fields = ('customer__user__username', 'boutique__name', 'status')
    list_filter = ('status', 'created_at', 'updated_at')

@admin.register(QuoteItem)
class QuoteItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'quote', 'product', 'quantity', 'price', 'status', 'created_at', 'updated_at')
    search_fields = ('quote__id', 'product__name', 'status')
    list_filter = ('status', 'created_at', 'updated_at')
