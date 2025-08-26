from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ContactForm, Subscription, BodyMeasurements
from .serializers import (
    ContactFormSerializer,
    SubscriptionSerializer,
    BodyMeasurementsSerializer
)


class ContactFormCreateView(generics.CreateAPIView):
    """
    API view to create a new contact form submission
    """
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': ('Thank you for contacting us. '
                            'We will get back to you soon.'),
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class SubscriptionCreateView(generics.CreateAPIView):
    """
    API view to create a new subscription
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': ('Thank you for subscribing to SmartFit! '
                            'Get ready for personalized workouts, '
                            'smart diet plans, and real-time support.'),
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BodyMeasurementsCreateView(generics.CreateAPIView):
    """
    API view to create a new body measurements submission
    """
    queryset = BodyMeasurements.objects.all()
    serializer_class = BodyMeasurementsSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': ('Thank you for submitting your body measurements. '
                            'This information will help us create a '
                            'personalized fitness plan for you.'),
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )