from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    platform = models.CharField(max_length=255, blank=True)
    contact = models.CharField(max_length=255, blank=True)
    img = models.ImageField(upload_to='img/indexes/contacts/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts_created', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    class Meta:
        ordering = ['platform']
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

    def __str__(self):
        return f"{self.platform}: {self.contact}"