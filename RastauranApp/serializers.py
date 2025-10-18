from rest_framework import serializers
from .models import Restaurant, Menu, Dish, Customer, Address, Driver, Order, OrderItem, Delivery, Payment


class CustomDepthMenu(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = 'name'


class CustomDeptCustomer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = 'first_name'


class CustomDepthAddress(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['city','region']


class CustomDepthRestauran(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = 'name'


class CustomDepthOrder(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = 'status'


class CustomDepthDish(serializers.ModelSerializer):
    class Meta:
        model  = Dish
        fields = 'name'


class CustomDepthDelivery(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['status','eta_minutes']

class CustomDepthPayment(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount','status']


class CustomDepthDriver(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['first_name', 'phone', 'created_at']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    restaurant = CustomDepthRestauran()

    class Meta:
        model = Menu
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    restaurant = CustomDepthRestauran()

    class Meta:
        model = Dish
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    customer = CustomDeptCustomer()
    restaurant = CustomDepthRestauran()

    class Meta:
        model = Address
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    restaurant = CustomDepthRestauran()
    
    class Meta:
        model = Driver
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    restaurant = CustomDepthRestauran()
    delivery_address = CustomDepthAddress()

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    order = CustomDepthOrder()
    dish = CustomDepthDish

    class Meta:
        model = OrderItem
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    driver_track = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Delivery
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    order = CustomDepthOrder()

    class Meta:
        model = Payment
        fields = '__all__'