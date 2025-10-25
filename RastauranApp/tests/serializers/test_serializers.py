from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from RastauranApp.models import Restaurant, Customer, Comment, Menu, Dish
from RastauranApp.serializers import RestaurantSerializer, CommentSerializer, MenuSerializer

class RestaurantSerializerTest(TestCase):
    def setUp(self):
        self.restaurant_data = {
            'name': 'Test Restaurant',
            'phone': '+123456789',
            'email': 'test@example.com',
            'description': 'Test description',
            'rating': 4.5,
            'is_active': True
        }
    
    def test_restaurant_serializer_create(self):
        serializer = RestaurantSerializer(data=self.restaurant_data)
        self.assertTrue(serializer.is_valid())
        restaurant = serializer.save()
        self.assertEqual(restaurant.name, 'Test Restaurant')
    
    def test_restaurant_serializer_validation(self):
        invalid_data = self.restaurant_data.copy()
        invalid_data['rating'] = 6.0  
        serializer = RestaurantSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        
        invalid_data = self.restaurant_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = RestaurantSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

class CommentSerializerTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            email='test@example.com'
        )
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
    
    def test_comment_serializer(self):
        comment_data = {
            'customer': self.customer.id,
            'restaurant': self.restaurant.id,
            'text': 'Great food!',
            'rating': 5
        }
        serializer = CommentSerializer(data=comment_data)
        self.assertTrue(serializer.is_valid())