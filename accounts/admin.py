from django.contrib import admin
from .models.members import MemberProfile, MemberBodyProfile
from .models.boutiques import BoutiqueProfile, BoutiqueCustomer


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'created_at', 'updated_at')
    search_fields = ('user__username', 'phone', 'address')
    list_filter = ('created_at', 'updated_at')


@admin.register(MemberBodyProfile)
class MemberBodyProfileAdmin(admin.ModelAdmin):
    list_display = ('member', 'height', 'weight', 'chest', 'waist', 'hips', 'created_at', 'updated_at')
    search_fields = ('member__user__username',)
    list_filter = ('created_at', 'updated_at')


@admin.register(BoutiqueProfile)
class BoutiqueProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('status', 'created_at', 'updated_at')


@admin.register(BoutiqueCustomer)
class BoutiqueCustomerAdmin(admin.ModelAdmin):
    list_display = ('boutique', 'user', 'is_active', 'created_at', 'updated_at')
    search_fields = ('boutique__name', 'user__username')
    list_filter = ('is_active', 'created_at', 'updated_at')