from rest_framework import serializers
from .models import Restaurant, Menu, Dish, Customer, Address, Driver, Order, OrderItem, Delivery, Payment, Comment, Reaction

class CustomDepthRestaurant(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name']

class CustomDepthCustomer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name']

class CustomDepthAddress(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['city','region']

class CustomDepthOrder(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class CustomDepthDish(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['name']

class RestaurantSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            "id", "name", "phone", "email", "description", "rating",
            "created_at", "updated_at", "is_active", "comments_count"
        ]
        read_only_fields = ["comments_count"]

class MenuSerializer(serializers.ModelSerializer):
    restaurant = CustomDepthRestaurant()

    class Meta:
        model = Menu
        fields = '__all__'

class DishSerializer(serializers.ModelSerializer):
    restaurant = CustomDepthRestaurant()

    class Meta:
        model = Dish
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    customer = CustomDepthCustomer()
    restaurant = CustomDepthRestaurant()

    class Meta:
        model = Address
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    restaurant = CustomDepthRestaurant()
    
    class Meta:
        model = Driver
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    restaurant = CustomDepthRestaurant()
    delivery_address = CustomDepthAddress()

    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    order = CustomDepthOrder()
    dish = CustomDepthDish()

    class Meta:
        model = OrderItem
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    order = CustomDepthOrder()

    class Meta:
        model = Payment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id", "customer", "author", "restaurant", "text", "rating",
            "created_at", "updated_at", "is_active", "likes", "dislikes"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "likes", "dislikes", "author"]

    def get_likes(self, obj):
        return obj.reactions.filter(is_like=True).count()

    def get_dislikes(self, obj):
        return obj.reactions.filter(is_like=False).count()

    def get_author(self, obj):
        return {
            "id": obj.customer.id,
            "first_name": obj.customer.first_name,
            "last_name": obj.customer.last_name,
        }