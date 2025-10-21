from rest_framework import generics
from rest_framework import serializers
from .models import Restaurant, Menu, Dish, Customer, Address, Driver, Order, OrderItem, Delivery, Payment, Comment, ReactionOfRestaurant
from .serializers import RestaurantSerializer, MenuSerializer, DishSerializer, CustomerSerializer, AddressSerializer, DriverSerializer, OrderSerializer, OrderItemSerializer, DeliverySerializer, PaymentSerializer,CommentSerializer, RestaurantSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

class RestaurantList(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantDetail(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuList(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuDetail(generics.RetrieveAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class DishList(generics.ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DishDetail(generics.RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class AddressList(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AddressDetail(generics.RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class DriverList(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class DriverDetail(generics.RetrieveAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemList(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemDetail(generics.RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class DeliveryList(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class DeliveryDetail(generics.RetrieveAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetail(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class RestaurantCommentsListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        restaurant_id = self.kwargs["restaurant_id"]
        return Comment.objects.filter(restaurant_id=restaurant_id).annotate(
            likes=Count('reactions', filter=Q(reactions__is_like=True)),
            dislikes=Count('reactions', filter=Q(reactions__is_like=False))
        )

    def perform_create(self, serializer):
        restaurant_id = self.kwargs["restaurant_id"]
        serializer.save(restaurant_id=restaurant_id)


class RestaurantRetrieveView(generics.RetrieveAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.annotate(
            comments_count=Count('comments')
        )


class CommentReactView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        customer_id = request.data.get("customer_id")
        is_like = request.data.get("is_like")

        if not customer_id or is_like is None:
            return Response(
                {"detail": "Нужно указать customer_id и is_like (true/false)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comment = get_object_or_404(Comment, id=comment_id)

        reaction, created = ReactionOfRestaurant.objects.get_or_create(
            customer_id=customer_id,
            comment=comment,
            defaults={"is_like": bool(is_like)},
        )

        if created:
            return Response({"status": "создано", "is_like": reaction.is_like})

        if reaction.is_like == bool(is_like):
            reaction.delete()
            return Response({"status": "удалено"})
        else:
            reaction.is_like = bool(is_like)
            reaction.save()
            return Response({"status": "обновлено", "is_like": reaction.is_like})
