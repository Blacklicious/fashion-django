from django.contrib import admin
from .models import Product, ProductCategory

# Register your models here.

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id','name','boutique', 'parent', 'created_by', 'updated_at'
    )
    search_fields = ('name', 'slug', 'description')
    list_filter = (
        'status', 'is_featured',
        'created_at', 'updated_at'
    )
    raw_id_fields = ('parent', 'created_by')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': (
                'boutique','name', 'slug', 'description',
                'img1', 'parent', 'created_by'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'sku', 'boutique', 'category',
        'price', 'price_discount', 'status', 'quantity',
        'created_at'
    )
    search_fields = ('name', 'sku', 'tags', 'notes')
    list_filter = (
        'status', 'boutique', 'category',
        'created_at', 'updated_at'
    )
    raw_id_fields = (
        'boutique', 'category',
        'parent_product', 'created_by'
    )
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': (
                'name', 'sku', 'description',
                'tags', 'notes', 'status'
            )
        }),
        ('Pricing & Stock', {
            'fields': (
                'price', 'price_discount',
                'quantity'
            )
        }),
        ('Relations', {
            'fields': (
                'boutique', 'category',
                'parent_product', 'created_by'
            )
        }),
        ('Images', {
            'fields': (
                'img1', 'img2', 'img3',
                'img4', 'img5', 'img6'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
