from rest_framework import serializers
from .models import ContactForm, Subscription, BodyMeasurements


class ContactFormSerializer(serializers.ModelSerializer):
    """
    Serializer for the ContactForm model
    """
    class Meta:
        model = ContactForm
        fields = ['id', 'name', 'email', 'query_type', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        """
        Validate that the name is not empty and has a reasonable length
        """
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Name must be at least 2 characters long")
        return value

    def validate_message(self, value):
        """
        Validate that the message is not empty and has a reasonable length
        """
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Message must be at least 10 characters long")
        return value


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subscription model
    """
    class Meta:
        model = Subscription
        fields = ['id', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_email(self, value):
        """
        Validate that the email is not already subscribed
        """
        if Subscription.objects.filter(
                email=value,
                status='ACT'
        ).exists():
            raise serializers.ValidationError(
                "This email is already subscribed")
        return value


class BodyMeasurementsSerializer(serializers.ModelSerializer):
    """
    Serializer for the BodyMeasurements model
    """
    class Meta:
        model = BodyMeasurements
        fields = [
            'id', 'name', 'email', 'height', 'weight',
            'waist_circumference', 'hip_circumference',
            'chest_circumference', 'arm_circumference',
            'thigh_circumference', 'neck_circumference',
            'photo', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        """
        Validate that the name is not empty and has a reasonable length
        """
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Name must be at least 2 characters long")
        return value
