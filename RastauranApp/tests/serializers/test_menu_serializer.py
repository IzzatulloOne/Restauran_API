from django.test import TestCase
from RastauranApp.models import Restaurant, Menu
from RastauranApp.serializers import MenuSerializer


class MenuSerializerTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Pizza Palace',
            phone='+1234567890'
        )
        
        self.menu_data = {
            'restaurant': self.restaurant,
            'name': 'Main Menu',
            'description': 'Our main menu with all dishes',
            'is_active': True
        }
        self.menu = Menu.objects.create(**self.menu_data)

    def test_menu_serializer_contains_expected_fields(self):
        serializer = MenuSerializer(instance=self.menu)
        data = serializer.data
        
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('description', data)
        self.assertIn('is_active', data)
        self.assertIn('created_at', data)
        self.assertIn('restaurant', data)

    def test_menu_serializer_restaurant_field(self):
        serializer = MenuSerializer(instance=self.menu)
        restaurant_data = serializer.data['restaurant']
        
        self.assertEqual(restaurant_data['name'], 'Pizza Palace')

    def test_menu_serializer_data_correctness(self):
        serializer = MenuSerializer(instance=self.menu)
        
        self.assertEqual(serializer.data['name'], self.menu_data['name'])
        self.assertEqual(serializer.data['description'], self.menu_data['description'])
        self.assertEqual(serializer.data['is_active'], self.menu_data['is_active'])