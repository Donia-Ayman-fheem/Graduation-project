from django.urls import path, include
from . import api

app_name = 'shopping'

# API URL patterns
api_urlpatterns = [
    # Product endpoints
    path('products/', api.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', api.ProductDetailView.as_view(), name='product_detail'),
    
    # Cart endpoints
    path('cart/', api.CartView.as_view(), name='cart'),
    path('cart/items/', api.CartItemView.as_view(), name='cart_item_add'),
    path('cart/items/<int:pk>/', api.CartItemView.as_view(), name='cart_item_detail'),
    
    # Checkout endpoint
    path('checkout/', api.CheckoutView.as_view(), name='checkout'),
    
    # Order endpoints
    path('orders/', api.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', api.OrderDetailView.as_view(), name='order_detail'),
]

urlpatterns = [
    # API endpoints
    path('api/', include((api_urlpatterns, 'api'))),
]
