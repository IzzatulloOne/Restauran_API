from django.test import TestCase
from django.core.exceptions import ValidationError
from RastauranApp.models import Restaurant, Customer, Comment, Menu, Dish, Order, OrderItem, Reaction

class RestaurantModelTest(TestCase):
    def test_create_restaurant(self):
        restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            phone='+123456789',
            email='test@example.com',
            rating=4.5
        )
        self.assertEqual(str(restaurant), 'Test Restaurant')
        self.assertTrue(restaurant.is_active)
    
    def test_restaurant_rating_validation(self):
        restaurant = Restaurant(rating=6.0)  
        with self.assertRaises(ValidationError):
            restaurant.full_clean()

class CommentModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
    
    def test_create_comment(self):
        comment = Comment.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            text='Great food!',
            rating=5
        )
        self.assertEqual(str(comment), f'Comment by {self.customer} on {self.restaurant}')
        self.assertTrue(comment.is_active)

class ReactionModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        self.comment = Comment.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            text='Test comment',
            rating=5
        )
    
    def test_create_reaction(self):
        reaction = Reaction.objects.create(
            customer=self.customer,
            comment=self.comment,
            is_like=True
        )
        self.assertEqual(str(reaction), f'{self.customer} Like comment {self.comment.id}')
    
    def test_unique_reaction_constraint(self):
        Reaction.objects.create(
            customer=self.customer,
            comment=self.comment,
            is_like=True
        )
        
        with self.assertRaises(Exception):  
            Reaction.objects.create(
                customer=self.customer,
                comment=self.comment,
                is_like=False
            )