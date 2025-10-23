from django.test import TestCase
from RastauranApp.models import Restaurant, Customer, Comment, Reaction
from RastauranApp.serializers import CommentSerializer


class CommentSerializerTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            phone='+1234567890'
        )
        
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        
        self.comment = Comment.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            text='Great food and service!',
            rating=5
        )
        
        Reaction.objects.create(
            customer=self.customer,
            comment=self.comment,
            is_like=True
        )
        
        another_customer = Customer.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com'
        )
        Reaction.objects.create(
            customer=another_customer,
            comment=self.comment,
            is_like=False
        )

    def test_comment_serializer_fields(self):
        serializer = CommentSerializer(instance=self.comment)
        data = serializer.data
        
        expected_fields = [
            "id", "customer", "author", "restaurant", "text", "rating",
            "created_at", "updated_at", "is_active", "likes", "dislikes"
        ]
        
        for field in expected_fields:
            self.assertIn(field, data)

    def test_comment_serializer_likes_dislikes_count(self):
        serializer = CommentSerializer(instance=self.comment)
        
        self.assertEqual(serializer.data['likes'], 1)
        self.assertEqual(serializer.data['dislikes'], 1)

    def test_comment_serializer_author_field(self):
        serializer = CommentSerializer(instance=self.comment)
        author_data = serializer.data['author']
        
        self.assertEqual(author_data['id'], self.customer.id)
        self.assertEqual(author_data['first_name'], self.customer.first_name)
        self.assertEqual(author_data['last_name'], self.customer.last_name)