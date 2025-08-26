from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from decimal import Decimal
from .models import Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    CheckoutSerializer
)


class ProductListView(generics.ListAPIView):
    """
    API view to list all products
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Apply category filter if provided
        category = request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
            
        # Apply search filter if provided
        search = request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        # Apply featured filter if provided
        featured = request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Products retrieved successfully',
            'data': serializer.data
        })


class ProductDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific product with all its details
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': 'Product details retrieved successfully',
            'data': serializer.data
        })


class CartView(APIView):
    """
    API view to view and manage the user's cart
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get user's cart or create if it doesn't exist"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response({
            'message': 'Cart retrieved successfully',
            'data': serializer.data
        })


class CartItemView(APIView):
    """
    API view to add, update, or remove items from the cart
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Add item to cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))
            
            # Check if product exists and is active
            product = get_object_or_404(Product, id=product_id, is_active=True)
            
            # Check if product is in stock
            if product.stock < quantity:
                return Response({
                    'error': f'Not enough stock. Only {product.stock} available.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if item already in cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            # If item already exists, update quantity
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return Response({
                'message': f'{product.name} added to cart',
                'data': CartSerializer(cart).data
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        """Update cart item quantity"""
        if not pk:
            return Response({
                'error': 'Cart item ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)
        
        quantity = request.data.get('quantity')
        if not quantity or int(quantity) < 1:
            return Response({
                'error': 'Quantity must be at least 1'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        quantity = int(quantity)
        
        # Check if product is in stock
        if cart_item.product.stock < quantity:
            return Response({
                'error': f'Not enough stock. Only {cart_item.product.stock} available.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response({
            'message': 'Cart item updated',
            'data': CartSerializer(cart).data
        })
    
    def delete(self, request, pk=None):
        """Remove item from cart"""
        if not pk:
            return Response({
                'error': 'Cart item ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)
        cart_item.delete()
        
        return Response({
            'message': 'Item removed from cart',
            'data': CartSerializer(cart).data
        })


class CheckoutView(APIView):
    """
    API view to process checkout
    """
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        """Process checkout"""
        # Get user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({
                'error': 'Your cart is empty'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if cart has items
        if cart.items.count() == 0:
            return Response({
                'error': 'Your cart is empty'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate checkout data
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate total amount
        total_amount = Decimal('0.00')
        cart_items = cart.items.all()
        
        # Check stock for all items
        for item in cart_items:
            if item.product.stock < item.quantity:
                return Response({
                    'error': f'Not enough stock for {item.product.name}. Only {item.product.stock} available.'
                }, status=status.HTTP_400_BAD_REQUEST)
            total_amount += item.get_total_price
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=serializer.validated_data['full_name'],
            email=serializer.validated_data['email'],
            phone=serializer.validated_data['phone'],
            address=serializer.validated_data['address'],
            city=serializer.validated_data['city'],
            postal_code=serializer.validated_data.get('postal_code', ''),
            country=serializer.validated_data['country'],
            notes=serializer.validated_data.get('notes', ''),
            total_amount=total_amount
        )
        
        # Create order items and update stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_final_price
            )
            
            # Update product stock
            item.product.stock -= item.quantity
            item.product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        return Response({
            'message': 'Order placed successfully',
            'data': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    """
    API view to list user's orders
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Orders retrieved successfully',
            'data': serializer.data
        })


class OrderDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific order with all its details
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': 'Order details retrieved successfully',
            'data': serializer.data
        })
