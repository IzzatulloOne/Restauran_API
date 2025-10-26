from rest_framework.test import APITestCase
from RastauranApp.models import Restaurant
from RastauranApp.serializers import RestaurantSerializer

class RestaurantSerializerTest(APITestCase):
    def test_serializer_fields(self):
        restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            phone='+123456789',
            email='noname4@gmail.com',
            description='Test description',
            rating=4.5,
            is_active=True
        )
        
        serializer = RestaurantSerializer(restaurant)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Test Restaurant')
        self.assertEqual(data['phone'], '+123456789')
        self.assertEqual(data['email'], 'noname3@gmail.com')
        self.assertEqual(data['description'], 'Test description')
        self.assertEqual(data['rating'], 4.5)
        self.assertEqual(data['is_active'], True)

    def test_serializer_many_objects(self):
        Restaurant.objects.create(name='First', rating=4.0)
        Restaurant.objects.create(name='Second', rating=4.5)
        
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        
        self.assertEqual(len(serializer.data), 2)
        self.assertEqual(serializer.data[0]['name'], 'First')
        self.assertEqual(serializer.data[1]['name'], 'Second')

    def test_serializer_validation(self):
        valid_data = {
            'name': 'NoName Restaurant',
            'phone': '+123456789',
            'email': 'noname2@gmail.com',
            'rating': 4.5
        }
        serializer = RestaurantSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

        invalid_data = {
            'name': 'noName Restaurant',
            'phone': '+123456789',
            'email': 'noName@gmail.com',
            'rating': 6.0 
        }
        serializer = RestaurantSerializer(data=invalid_data)
        self.assertEqual(serializer.is_valid(), False)