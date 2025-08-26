from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product, Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['get_total_price']
    fields = ('product', 'quantity', 'get_total_price')

    def get_total_price(self, obj):
        return obj.get_total_price
    get_total_price.short_description = _('Total Price')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total_price']
    fields = ('product', 'quantity', 'price', 'get_total_price')

    def get_total_price(self, obj):
        return obj.get_total_price
    get_total_price.short_description = _('Total Price')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'stock', 'is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'image')
        }),
        (_('Pricing and Stock'), {
            'fields': ('price', 'discount_price', 'stock')
        }),
        (_('Status'), {
            'fields': ('is_featured', 'is_active')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_cart_items_count', 'get_cart_total', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]

    def get_cart_items_count(self, obj):
        return obj.get_cart_items_count
    get_cart_items_count.short_description = _('Items Count')

    def get_cart_total(self, obj):
        return obj.get_cart_total
    get_cart_total.short_description = _('Total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'address')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        (None, {
            'fields': ('user', 'status', 'total_amount')
        }),
        (_('Customer Information'), {
            'fields': ('full_name', 'email', 'phone')
        }),
        (_('Shipping Information'), {
            'fields': ('address', 'city', 'postal_code', 'country')
        }),
        (_('Additional Information'), {
            'fields': ('notes',)
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
