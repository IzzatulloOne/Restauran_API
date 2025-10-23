from django.test import TestCase
from ..models import Restaurant
from ..serializers import RestaurantSerializer


class RestaurantSerializerTest(TestCase):
    def setUp(self):
        self.restaurant_data = {
            'name': 'Test Restaurant',
            'phone': '+1234567890',
            'email': 'test@restaurant.com',
            'description': 'A test restaurant',
            'rating': 4.5,
            'is_active': True
        }
        self.restaurant = Restaurant.objects.create(**self.restaurant_data)

    def test_restaurant_serializer_contains_expected_fields(self):
        """Тест проверяет наличие всех ожидаемых полей в сериализаторе"""
        serializer = RestaurantSerializer(instance=self.restaurant)
        data = serializer.data
        
        expected_fields = [
            "id", "name", "phone", "email", "description", "rating",
            "created_at", "updated_at", "is_active", "comments_count"
        ]
        
        for field in expected_fields:
            self.assertIn(field, data)

    def test_restaurant_serializer_field_values(self):
        """Тест проверяет корректность значений полей"""
        serializer = RestaurantSerializer(instance=self.restaurant)
        
        self.assertEqual(serializer.data['name'], self.restaurant_data['name'])
        self.assertEqual(serializer.data['phone'], self.restaurant_data['phone'])
        self.assertEqual(serializer.data['email'], self.restaurant_data['email'])
        self.assertEqual(float(serializer.data['rating']), self.restaurant_data['rating'])