from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from RastauranApp.models import Restaurant

class RestaurantAPITest(APITestCase):
    def setUp(self):
    
        self.restaurant1 = Restaurant.objects.create(
            name='Pizza Palace', 
            description='Best pizza in town', 
            rating=4.5, 
            is_active=True
        )
        self.restaurant2 = Restaurant.objects.create(
            name='Burger King', 
            description='Great burgers', 
            rating=4.2, 
            is_active=True
        )
        self.restaurant3 = Restaurant.objects.create(
            name='Sushi Spot', 
            description='Fresh sushi', 
            rating=4.8, 
            is_active=False
        )
        
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)

    def test_search_restaurant_by_name(self):
        response = self.client.get(reverse('restaurant-list'), {'search': 'pizza'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Pizza Palace')

    def test_search_restaurant_by_description(self):
        response = self.client.get(reverse('restaurant-list'), {'search': 'burgers'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Burger King')

    def test_filter_restaurant_by_active(self):
        response = self.client.get(reverse('restaurant-list'), {'is_active': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_filter_restaurant_by_rating(self):
        response = self.client.get(reverse('restaurant-list'), {'rating': 4.5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Pizza Palace')

    def test_session_authentication(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(response.status_code, 200)

    def test_session_authentication_fail(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(response.status_code, 200) 

    def test_token_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(response.status_code, 200)

    def test_token_authentication_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        response = self.client.get(reverse('restaurant-list'))
        self.assertNotEqual(response.status_code, 200)  

    def test_create_restaurant(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'name': 'New Restaurant',
            'phone': '+123456789',
            'email': 'new@example.com',
            'description': 'New restaurant description',
            'rating': 4.2,
            'is_active': True
        }
        response = self.client.post(reverse('restaurant-list'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Restaurant.objects.count(), 4)

    def test_update_restaurant(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'name': 'Updated Pizza Palace',
            'phone': self.restaurant1.phone,
            'email': self.restaurant1.email,
            'description': 'Updated description',
            'rating': 4.7,
            'is_active': True
        }
        response = self.client.put(reverse('restaurant-detail', args=[self.restaurant1.id]), data)
        self.assertEqual(response.status_code, 200)
        self.restaurant1.refresh_from_db()
        self.assertEqual(self.restaurant1.name, 'Updated Pizza Palace')

    def test_partial_update_restaurant(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {'rating': 4.9}
        response = self.client.patch(reverse('restaurant-detail', args=[self.restaurant1.id]), data)
        self.assertEqual(response.status_code, 200)
        self.restaurant1.refresh_from_db()
        self.assertEqual(self.restaurant1.rating, 4.9)

    def test_delete_restaurant(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(reverse('restaurant-detail', args=[self.restaurant1.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Restaurant.objects.count(), 2)