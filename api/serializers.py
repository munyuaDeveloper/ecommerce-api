from rest_framework import serializers
from .models import Product, ShoppingCart


class CartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, max_value=100)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'product', 'quantity']


class ProductSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()
    price = serializers.DecimalField(min_value=1.00, max_digits=None, decimal_places=2)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'quantity', 'image', 'price', 'available', 'cart_items']

    def get_cart_items(self, instance):
        items = ShoppingCart.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data
