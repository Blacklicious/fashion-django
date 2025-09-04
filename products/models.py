import os
from django.db import models
from django.contrib.auth.models import User
from accounts.models.boutiques import BoutiqueProfile

# Create your models here.

#--------------------------------------------------------------------------------------------------------------------------
#------------------------------------- product image upload function ------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------

def product_image_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    #remane using number
    new_filename = f"{instance.sku}_{instance.id}{ext}"
    return os.path.join('img/products/', new_filename)

#--------------------------------------------------------------------------------------------------------------------------
#------------------------------------- product category model -------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------

class ProductCategory(models.Model):
    boutique = models.ForeignKey(BoutiqueProfile, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)  
    img1 = models.ImageField(upload_to='img/indexes/categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories_created', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
#--------------------------------------------------------------------------------------------------------------------------
#-------------------------------------- product model ---------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------

class Product(models.Model):
    #-------- product filters
    boutique = models.ForeignKey(BoutiqueProfile, on_delete=models.CASCADE, related_name='products')
    #-------- product categories
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    parent_product = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_products', null=True, blank=True)
    sku = models.CharField(max_length=255, blank=True)
    #-------- product details
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    #-------- product images (remane image with search friendly name)
    img1 = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    img2 = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    img3 = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    img4 = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    img5 = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    img6 = models.ImageField(upload_to=product_image_upload_to, blank=True, null=True)
    #-------- product stock
    quantity = models.PositiveIntegerField(default=0)
    #-------- product metadata
    tags = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products_created', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    class Meta:
        ordering = ['name']
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
    