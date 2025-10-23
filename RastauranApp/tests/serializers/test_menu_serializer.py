from django.test import TestCase
from ..models import Restaurant, Menu
from ..serializers import MenuSerializer


class MenuSerializerTest(TestCase):
    def setUp(self):
        # Создаем ресторан
        self.restaurant = Restaurant.objects.create(
            name='Pizza Palace',
            phone='+1234567890'
        )
        
        # Создаем меню
        self.menu_data = {
            'restaurant': self.restaurant,
            'name': 'Main Menu',
            'description': 'Our main menu with all dishes',
            'is_active': True
        }
        self.menu = Menu.objects.create(**self.menu_data)

    def test_menu_serializer_contains_expected_fields(self):
        """Тест проверяет наличие всех полей в сериализаторе меню"""
        serializer = MenuSerializer(instance=self.menu)
        data = serializer.data
        
        # Проверяем основные поля
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('description', data)
        self.assertIn('is_active', data)
        self.assertIn('created_at', data)
        self.assertIn('restaurant', data)

    def test_menu_serializer_restaurant_field(self):
        """Тест проверяет вложенное поле restaurant"""
        serializer = MenuSerializer(instance=self.menu)
        restaurant_data = serializer.data['restaurant']
        
        # Проверяем, что поле restaurant содержит имя ресторана
        self.assertEqual(restaurant_data, 'Pizza Palace')

    def test_menu_serializer_data_correctness(self):
        """Тест проверяет корректность данных меню"""
        serializer = MenuSerializer(instance=self.menu)
        
        self.assertEqual(serializer.data['name'], self.menu_data['name'])
        self.assertEqual(serializer.data['description'], self.menu_data['description'])
        self.assertEqual(serializer.data['is_active'], self.menu_data['is_active'])