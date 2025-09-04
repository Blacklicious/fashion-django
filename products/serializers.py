from products.models import Product, ProductCategory
from accounts.models.boutiques import BoutiqueProfile
from rest_framework import serializers
from django.contrib.auth.models import User

#--------------------------------------------------------------------------------------------------------------------------
#------------------------------------- product category serializer ------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------     
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
    
#--------------------------------------------------------------------------------------------------------------------------
#------------------------------------- product serializer -----------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)  # for output
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Product
        fields = '__all__'
