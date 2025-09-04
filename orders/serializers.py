from rest_framework import serializers
from .models.orders import Order, OrderItem
from .models.payments import Payment
from accounts.serializers import MemberProfileSerializer
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=OrderItem._meta.get_field('product').related_model.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_id', 'quantity', 'price', 'status', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    customer = MemberProfileSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'boutique', 'quote', 'status', 'payment_status',
            'total_amount', 'shipping_address', 'billing_address', 'notes', 'created_at', 'updated_at', 'items'
        ]

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'customer', 'boutique', 'amount', 'currency', 'payment_method',
            'status', 'stripe_payment_intent_id', 'stripe_charge_id', 'stripe_receipt_url',
            'paid_at', 'created_at', 'updated_at', 'notes'
        ]