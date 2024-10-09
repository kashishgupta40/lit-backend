from rest_framework import serializers
from .models import Product, Order, OrderItem, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price', 'is_paid', 'order_items']

    def get_order_items(self, obj):
        return [{'product': item.product.name, 'quantity': item.quantity, 'price': item.price} for item in obj.orderitem_set.all()]
