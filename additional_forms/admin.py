from django.contrib import admin
from .models import ContactForm, Subscription, BodyMeasurements


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'query_type', 'created_at')
    list_filter = ('query_type', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BodyMeasurements)
class BodyMeasurementsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'photo')
        }),
        ('Measurements', {
            'fields': (
                'height', 'weight', 'waist_circumference',
                'hip_circumference', 'chest_circumference',
                'arm_circumference', 'thigh_circumference',
                'neck_circumference'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
