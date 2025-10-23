from django.test import TestCase
from ..models import Restaurant, Customer, Comment, ReactionOfRestaurant
from ..serializers import CommentSerializer


class CommentSerializerTest(TestCase):
    def setUp(self):
        # Создаем ресторан
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            phone='+1234567890'
        )
        
        # Создаем клиента
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        
        # Создаем комментарий
        self.comment = Comment.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            text='Great food and service!',
            rating=5
        )
        
        # Создаем лайки и дизлайки для комментария
        ReactionOfRestaurant.objects.create(
            customer=self.customer,
            comment=self.comment,
            is_like=True
        )
        
        another_customer = Customer.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com'
        )
        ReactionOfRestaurant.objects.create(
            customer=another_customer,
            comment=self.comment,
            is_like=False
        )

    def test_comment_serializer_fields(self):
        """Тест проверяет поля сериализатора комментариев"""
        serializer = CommentSerializer(instance=self.comment)
        data = serializer.data
        
        expected_fields = [
            "id", "customer", "author", "restaurant", "text", "rating",
            "created_at", "updated_at", "is_active", "likes", "dislikes"
        ]
        
        for field in expected_fields:
            self.assertIn(field, data)

    def test_comment_serializer_likes_dislikes_count(self):
        """Тест проверяет корректный подсчет лайков и дизлайков"""
        serializer = CommentSerializer(instance=self.comment)
        
        # Должен быть 1 лайк и 1 дизлайк
        self.assertEqual(serializer.data['likes'], 1)
        self.assertEqual(serializer.data['dislikes'], 1)

    def test_comment_serializer_author_field(self):
        """Тест проверяет поле author с информацией о клиенте"""
        serializer = CommentSerializer(instance=self.comment)
        author_data = serializer.data['author']
        
        self.assertEqual(author_data['id'], self.customer.id)
        self.assertEqual(author_data['first_name'], self.customer.first_name)
        self.assertEqual(author_data['last_name'], self.customer.last_name)