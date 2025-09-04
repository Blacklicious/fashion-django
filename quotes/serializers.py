from rest_framework import serializers
from .models import Quote, QuoteItem
from products.models import Product

class QuoteItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = QuoteItem
        fields = ['id', 'product', 'quantity', 'price', 'status', 'created_at', 'updated_at']

class QuoteSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    boutique = serializers.StringRelatedField()
    items = QuoteItemSerializer(many=True, read_only=True)

    class Meta:
        model = Quote
        fields = ['id', 'customer', 'boutique', 'created_at', 'updated_at', 'status', 'items']