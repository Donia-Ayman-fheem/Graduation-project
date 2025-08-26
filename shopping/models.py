from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from decimal import Decimal


class ProductCategory(models.TextChoices):
    """
    Categories for shopping products
    """
    SUPPLEMENTS = 'SP', _('Supplements')
    EQUIPMENT = 'EQ', _('Equipment')
    CLOTHING = 'CL', _('Clothing')
    FOOD = 'FD', _('Food')
    BEVERAGES = 'BV', _('Beverages')
    ACCESSORIES = 'AC', _('Accessories')
    OTHER = 'OT', _('Other')


class Product(models.Model):
    """
    Model for products in the shopping list
    """
    name = models.CharField(_('Product Name'), max_length=200)
    description = models.TextField(_('Description'))
    category = models.CharField(
        _('Category'),
        max_length=2,
        choices=ProductCategory.choices,
        default=ProductCategory.OTHER
    )
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        _('Discount Price'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    stock = models.PositiveIntegerField(_('Stock'), default=0)
    image = models.ImageField(
        _('Product Image'),
        upload_to='products/images/',
        null=True,
        blank=True
    )
    is_featured = models.BooleanField(_('Featured'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def get_final_price(self):
        """Return the final price (considering discount if available)"""
        if self.discount_price:
            return self.discount_price
        return self.price

    @property
    def get_discount_percentage(self):
        """Calculate discount percentage if discount price is available"""
        if self.discount_price and self.price > 0:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return round(discount, 2)
        return 0


class Cart(models.Model):
    """
    Model for user's shopping cart
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f"{self.user.name}'s Cart"

    @property
    def get_cart_total(self):
        """Calculate total price of all items in cart"""
        cart_items = self.items.all()
        total = sum(item.get_total_price for item in cart_items)
        return total

    @property
    def get_cart_items_count(self):
        """Count total number of items in cart"""
        cart_items = self.items.all()
        count = sum(item.quantity for item in cart_items)
        return count


class CartItem(models.Model):
    """
    Model for items in a shopping cart
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def get_total_price(self):
        """Calculate total price for this cart item"""
        return self.product.get_final_price * Decimal(self.quantity)


class OrderStatus(models.TextChoices):
    """
    Status options for orders
    """
    PENDING = 'PD', _('Pending')
    PROCESSING = 'PR', _('Processing')
    SHIPPED = 'SH', _('Shipped')
    DELIVERED = 'DL', _('Delivered')
    CANCELLED = 'CN', _('Cancelled')


class Order(models.Model):
    """
    Model for user orders (checkout)
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    full_name = models.CharField(_('Full Name'), max_length=100)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=20)
    address = models.TextField(_('Address'))
    city = models.CharField(_('City'), max_length=100)
    postal_code = models.CharField(_('Postal Code'), max_length=20, blank=True, null=True)
    country = models.CharField(_('Country'), max_length=100)
    total_amount = models.DecimalField(_('Total Amount'), max_digits=10, decimal_places=2)
    status = models.CharField(
        _('Status'),
        max_length=2,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    notes = models.TextField(_('Notes'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.name}"


class OrderItem(models.Model):
    """
    Model for items in an order
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    price = models.DecimalField(_('Price at Purchase'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def get_total_price(self):
        """Calculate total price for this order item"""
        return self.price * Decimal(self.quantity)
