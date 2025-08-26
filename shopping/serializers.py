from rest_framework import serializers
from .models import Product, Cart, CartItem, Order, OrderItem


class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing products
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'price', 'discount_price', 'discount_percentage', 'final_price',
            'image', 'is_featured', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage

    def get_final_price(self, obj):
        return obj.get_final_price


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed product information
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'price', 'discount_price', 'discount_percentage', 'final_price',
            'stock', 'image', 'is_featured', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage

    def get_final_price(self, obj):
        return obj.get_final_price


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for cart items
    """
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_id', 'quantity', 'total_price', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_price(self, obj):
        return obj.get_total_price


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for shopping cart
    """
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total', 'items_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total(self, obj):
        return obj.get_cart_total

    def get_items_count(self, obj):
        return obj.get_cart_items_count


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for order items
    """
    product = ProductListSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_total_price(self, obj):
        return obj.get_total_price


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for orders
    """
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'full_name', 'email', 'phone', 'address', 'city',
            'postal_code', 'country', 'total_amount', 'status',
            'status_display', 'notes', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CheckoutSerializer(serializers.ModelSerializer):
    """
    Serializer for checkout process
    """
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone', 'address', 'city',
            'postal_code', 'country', 'notes'
        ]
