from django.db import models
from django.contrib.auth.models import User

class BoutiqueProfile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=512, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    social_media = models.JSONField(blank=True, null=True)  # Store social media links as JSON
    logo = models.ImageField(upload_to='img/boutiques/logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='img/boutiques/banners/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boutique_profiles_created', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "02 | Boutique"
        verbose_name_plural = "02 | Boutiques"
        ordering = ['name']


class BoutiqueCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='boutique_customer')
    boutique = models.ForeignKey(BoutiqueProfile, on_delete=models.CASCADE, related_name='customers')
    membership_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.boutique.name}"
    
    class Meta:
        verbose_name = "02 | Boutique customer"
        verbose_name_plural = "02 | Boutiques customers"
        unique_together = ('user', 'boutique')
        ordering = ['membership_date']