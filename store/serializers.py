from rest_framework import serializers
from .models import Product, Order, OrderItem, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'price', 'stock', 'image']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nested Product serializer

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)  # Use the OrderItemSerializer for nested order items

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price', 'is_paid', 'order_items']

    def to_representation(self, instance):
        """Customize the response to include order_items as a list of dictionaries."""
        representation = super().to_representation(instance)
        # Modify order_items to return a list of product names and details if needed
        order_items = representation.pop('order_items', [])
        representation['order_items'] = [
            {'product': item['product']['name'], 'quantity': item['quantity'], 'price': item['price']}
            for item in order_items
        ]
        return representation

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

