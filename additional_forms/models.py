from django.db import models
from django.utils.translation import gettext_lazy as _


class SubscriptionStatus(models.TextChoices):
    ACTIVE = 'ACT', _('Active')
    UNSUBSCRIBED = 'UNS', _('Unsubscribed')
    PENDING = 'PEN', _('Pending Confirmation')


class QueryType(models.TextChoices):
    GENERAL = 'GEN', _('General Inquiry')
    MEMBERSHIP = 'MEM', _('Membership Question')
    TECHNICAL = 'TEC', _('Technical Support')
    FEEDBACK = 'FDB', _('Feedback')
    OTHER = 'OTH', _('Other')


class ContactForm(models.Model):
    """
    Model for storing contact form submissions
    """
    name = models.CharField(_('Full Name'), max_length=100)
    email = models.EmailField(_('Email Address'))
    query_type = models.CharField(
        _('Query Type'),
        max_length=3,
        choices=QueryType.choices,
        default=QueryType.GENERAL
    )
    message = models.TextField(_('Message'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Contact Form')
        verbose_name_plural = _('Contact Forms')
        ordering = ['-created_at']

    def __str__(self):
        return (f"{self.name} - {self.get_query_type_display()} - "
                f"{self.created_at.strftime('%Y-%m-%d')}")


class Subscription(models.Model):
    """
    Model for storing email subscriptions for SmartFit updates
    """
    email = models.EmailField(_('Email Address'), unique=True)
    status = models.CharField(
        _('Status'),
        max_length=3,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} - {self.get_status_display()}"


class BodyMeasurements(models.Model):
    """
    Model for storing body measurements submissions
    """
    name = models.CharField(
        _('Full Name'),
        max_length=100
    )
    email = models.EmailField(
        _('Email Address')
    )
    height = models.DecimalField(
        _('Height (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    weight = models.DecimalField(
        _('Weight (kg)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    waist_circumference = models.DecimalField(
        _('Waist Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    hip_circumference = models.DecimalField(
        _('Hip Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    chest_circumference = models.DecimalField(
        _('Chest Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    arm_circumference = models.DecimalField(
        _('Arm Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    thigh_circumference = models.DecimalField(
        _('Thigh Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    neck_circumference = models.DecimalField(
        _('Neck Circumference (cm)'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    photo = models.ImageField(
        _('Full-body Photo'),
        upload_to='body_measurements/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Body Measurements')
        verbose_name_plural = _('Body Measurements')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"
