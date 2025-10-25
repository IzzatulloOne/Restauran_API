from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from RastauranApp.models import Restaurant, Customer, Comment, Reaction

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com'
        )
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            email='restaurant@example.com'
        )
    
    def test_token_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/token-test/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token_owner', response.data)
    
    def test_session_authentication(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/session-test/')
        self.assertEqual(response.status_code, 200)

class RestaurantCRUDTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='admin123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.restaurant_data = {
            'name': 'New Restaurant',
            'phone': '+123456789',
            'email': 'new@example.com',
            'description': 'New restaurant description',
            'rating': 4.2
        }
    
    def test_create_restaurant(self):
        response = self.client.post(
            '/api/restaurants/create/',
            self.restaurant_data,
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'New Restaurant')
    
    def test_update_restaurant(self):
        restaurant = Restaurant.objects.create(
            name='Old Name',
            email='old@example.com'
        )
        

        response = self.client.put(
            f'/api/restaurants/{restaurant.id}/update/',
            {'name': 'Updated Name', 'email': 'updated@example.com'},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        restaurant.refresh_from_db()
        self.assertEqual(restaurant.name, 'Updated Name')
    
    def test_partial_update_restaurant(self):
        restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            email='test@example.com'
        )
        
        response = self.client.patch(
            f'/api/restaurants/{restaurant.id}/update/',
            {'rating': 4.9},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        restaurant.refresh_from_db()
        self.assertEqual(restaurant.rating, 4.9)
    
    def test_delete_restaurant(self):
        restaurant = Restaurant.objects.create(
            name='To Delete',
            email='delete@example.com'
        )
        
        response = self.client.delete(f'/api/restaurants/{restaurant.id}/delete/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Restaurant.objects.count(), 0)

class SearchFilterTests(APITestCase):
    def setUp(self):
        Restaurant.objects.create(name='Pizza Palace', description='Best pizza in town', rating=4.5, is_active=True)
        Restaurant.objects.create(name='Burger King', description='Great burgers', rating=4.2, is_active=True)
        Restaurant.objects.create(name='Sushi Spot', description='Fresh sushi', rating=4.8, is_active=False)
    
    def test_search_functionality(self):
        response = self.client.get('/api/restaurants/?search=pizza')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Pizza Palace')
    
    def test_filter_functionality(self):
        response = self.client.get('/api/restaurants/?is_active=true')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    def test_ordering_functionality(self):
        response = self.client.get('/api/restaurants/?ordering=-rating')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Sushi Spot')