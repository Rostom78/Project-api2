from rest_framework import serializers
from .models import VideoGame, Cart, CartItem, Order, OrderItem

# Serializer for VideoGame
class VideoGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGame
        fields = '__all__'

# Serializer for Cart and Cart Items
class CartItemSerializer(serializers.ModelSerializer):
    game = VideoGameSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

# Serializer for Orders and Order Items
class OrderItemSerializer(serializers.ModelSerializer):
    game = VideoGameSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
