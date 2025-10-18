# admin.py
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html
import csv

from .models import (
    Restaurant, Menu, Dish, Customer, Address,
    Driver, Order, OrderItem, Delivery, Payment
)


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    fields = ("label", "street", "city", "region", "country")
    readonly_fields = ()
    show_change_link = True


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("name", "dish", "unit_price", "quantity", "total_price", "created_at")
    readonly_fields = ("total_price", "created_at")
    raw_id_fields = ("dish",)
    show_change_link = False


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ("provider", "amount", "currency", "status", "transaction_id", "paid_at", "created_at")
    readonly_fields = ("created_at", "paid_at")
    show_change_link = False


class DeliveryInline(admin.StackedInline):
    model = Delivery
    extra = 0
    fields = ("driver", "status", "assigned_at", "picked_at", "delivered_at", "eta_minutes")
    readonly_fields = ("assigned_at", "picked_at", "delivered_at")
    raw_id_fields = ("driver",)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email", "rating", "is_active", "created_at")
    search_fields = ("name", "phone", "email")
    list_filter = ("is_active",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "description")}),
        ("Contacts", {"fields": ("phone", "email")}),
        ("Meta", {"fields": ("rating", "is_active", "created_at", "updated_at")}),
    )
    save_on_top = True
    list_per_page = 25


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "restaurant", "is_active", "created_at")
    search_fields = ("name", "restaurant__name")
    list_filter = ("is_active", "restaurant")
    raw_id_fields = ("restaurant",)
    list_select_related = ("restaurant",)
    readonly_fields = ("created_at",)
    list_per_page = 25


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "restaurant", "price_display", "currency", "is_available", "prep_time_minutes", "created_at")
    search_fields = ("name", "restaurant__name")
    list_filter = ("is_available", "currency", "restaurant")
    raw_id_fields = ("restaurant", "menu")
    list_select_related = ("restaurant", "menu")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("is_available",)
    ordering = ("-created_at",)
    list_per_page = 30

    def price_display(self, obj):
        return f"{obj.price} {obj.currency}"
    price_display.short_description = "Price"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone", "is_active", "created_at")
    search_fields = ("first_name", "last_name", "email", "phone")
    list_filter = ("is_active",)
    readonly_fields = ("created_at", "updated_at")
    inlines = (AddressInline,)
    ordering = ("-created_at",)
    list_per_page = 25


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "street", "city", "region", "country", "customer", "restaurant", "created_at")
    search_fields = ("street", "city", "label", "customer__first_name", "restaurant__name")
    raw_id_fields = ("customer", "restaurant")
    list_select_related = ("customer", "restaurant")
    readonly_fields = ("created_at",)
    list_per_page = 25


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "phone", "restaurant", "is_active", "created_at")
    search_fields = ("first_name", "last_name", "phone", "vehicle_info")
    list_filter = ("is_active", "restaurant")
    raw_id_fields = ("restaurant",)
    list_select_related = ("restaurant",)
    readonly_fields = ("created_at",)
    list_per_page = 25


def _export_orders_as_csv(modeladmin, request, queryset):
    """
    Export selected orders to CSV. Includes basic fields + status integer.
    """
    fieldnames = [
        "id", "customer_id", "customer_name", "restaurant_id", "restaurant_name",
        "total_amount", "currency", "status", "placed_at", "updated_at", "notes"
    ]
    ts = timezone.now().strftime("%Y%m%d_%H%M%S")
    filename = f"orders_export_{ts}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(fieldnames)
    for order in queryset.select_related("customer", "restaurant"):
        writer.writerow([
            order.id,
            order.customer.id,
            f"{order.customer.first_name} {order.customer.last_name or ''}".strip(),
            order.restaurant.id,
            order.restaurant.name,
            order.total_amount,
            order.currency,
            order.status,
            order.placed_at.isoformat() if order.placed_at else "",
            order.updated_at.isoformat() if order.updated_at else "",
            order.notes or "",
        ])
    return response
_export_orders_as_csv.short_description = "Export selected orders as CSV"


def _mark_orders_processing(modeladmin, request, queryset):
    updated = queryset.update(status=1, updated_at=timezone.now())
    modeladmin.message_user(request, f"{updated} order(s) marked as Processing.")
_mark_orders_processing.short_description = "Mark selected orders as Processing"


def _mark_orders_delivered(modeladmin, request, queryset):
    updated = queryset.update(status=2, updated_at=timezone.now())
    modeladmin.message_user(request, f"{updated} order(s) marked as Delivered.")
_mark_orders_delivered.short_description = "Mark selected orders as Delivered"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_link", "restaurant_link", "total_amount", "currency", "status", "placed_at")
    list_filter = ("status", "restaurant")
    search_fields = ("id", "customer__first_name", "customer__last_name", "customer__email", "restaurant__name")
    raw_id_fields = ("customer", "restaurant", "delivery_address")
    readonly_fields = ("placed_at", "updated_at")
    inlines = (OrderItemInline, PaymentInline, DeliveryInline)
    actions = (_export_orders_as_csv, _mark_orders_processing, _mark_orders_delivered)
    list_select_related = ("customer", "restaurant")
    ordering = ("-placed_at",)
    list_per_page = 25

    def customer_link(self, obj):
        if obj.customer_id:
            return format_html('<a href="{}">{}</a>', f"/admin/{obj._meta.app_label}/customer/{obj.customer_id}/change/", obj.customer)
        return "-"
    customer_link.short_description = "Customer"

    def restaurant_link(self, obj):
        if obj.restaurant_id:
            return format_html('<a href="{}">{}</a>', f"/admin/{obj._meta.app_label}/restaurant/{obj.restaurant_id}/change/", obj.restaurant.name)
        return "-"
    restaurant_link.short_description = "Restaurant"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "name", "unit_price", "quantity", "total_price", "created_at")
    search_fields = ("name", "order__id")
    raw_id_fields = ("order", "dish")
    readonly_fields = ("created_at",)
    list_select_related = ("order",)
    list_per_page = 50


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "driver", "status", "assigned_at", "picked_at", "delivered_at")
    search_fields = ("order__id", "driver__first_name", "driver__last_name")
    list_filter = ("status", "driver")
    raw_id_fields = ("order", "driver")
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("order", "driver")
    list_per_page = 25


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "provider", "amount", "currency", "status", "transaction_id", "paid_at")
    search_fields = ("transaction_id", "provider", "order__id")
    list_filter = ("status", "provider")
    raw_id_fields = ("order",)
    readonly_fields = ("created_at",)
    list_select_related = ("order",)
    list_per_page = 50