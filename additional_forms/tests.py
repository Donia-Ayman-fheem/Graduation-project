from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from .models import ContactForm, QueryType, Subscription, BodyMeasurements


class ContactFormAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.contact_form_url = reverse('additional_forms:api:contact_form')

        # Test contact form data
        self.valid_contact_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'query_type': QueryType.GENERAL,
            'message': 'This is a test message for the contact form API.'
        }

        self.invalid_contact_data = {
            'name': 'T',  # Too short
            'email': 'invalid-email',  # Invalid email
            'query_type': 'INVALID',  # Invalid choice
            'message': 'Short'  # Too short
        }

    def test_create_contact_form_valid_data(self):
        """Test creating a contact form with valid data"""
        response = self.client.post(
            self.contact_form_url,
            self.valid_contact_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactForm.objects.count(), 1)
        self.assertEqual(ContactForm.objects.get().name, 'Test User')
        self.assertEqual(ContactForm.objects.get().email, 'test@example.com')
        self.assertEqual(ContactForm.objects.get().query_type, QueryType.GENERAL)

    def test_create_contact_form_invalid_data(self):
        """Test creating a contact form with invalid data"""
        response = self.client.post(
            self.contact_form_url,
            self.invalid_contact_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContactForm.objects.count(), 0)


class SubscriptionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.subscription_url = reverse('additional_forms:api:subscription')

        # Test subscription data
        self.valid_subscription_data = {
            'email': 'subscriber@example.com'
        }

        self.invalid_subscription_data = {
            'email': 'invalid-email'  # Invalid email
        }

    def test_create_subscription_valid_data(self):
        """Test creating a subscription with valid data"""
        response = self.client.post(
            self.subscription_url,
            self.valid_subscription_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(Subscription.objects.get().email, 'subscriber@example.com')

    def test_create_subscription_invalid_data(self):
        """Test creating a subscription with invalid data"""
        response = self.client.post(
            self.subscription_url,
            self.invalid_subscription_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Subscription.objects.count(), 0)

    def test_duplicate_subscription(self):
        """Test that duplicate subscriptions are not allowed"""
        # Create the first subscription
        Subscription.objects.create(email='subscriber@example.com')

        # Try to create a duplicate
        response = self.client.post(
            self.subscription_url,
            self.valid_subscription_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Subscription.objects.count(), 1)


class BodyMeasurementsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.body_measurements_url = reverse('additional_forms:api:body_measurements')

        # Create a test image file
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=(
                b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,'
                b'\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
            ),
            content_type='image/jpeg'
        )

        # Test body measurements data
        self.valid_measurements_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'height': 180.5,
            'weight': 75.2,
            'waist_circumference': 85.0,
            'hip_circumference': 95.0,
            'chest_circumference': 100.0,
            'arm_circumference': 35.0,
            'thigh_circumference': 55.0,
            'neck_circumference': 40.0,
            'photo': self.test_image
        }

        self.invalid_measurements_data = {
            'name': 'T',  # Too short
            'email': 'invalid-email',  # Invalid email
        }

    def test_create_body_measurements_valid_data(self):
        """Test creating body measurements with valid data"""
        response = self.client.post(
            self.body_measurements_url,
            self.valid_measurements_data,
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BodyMeasurements.objects.count(), 1)
        self.assertEqual(BodyMeasurements.objects.get().name, 'Test User')
        body = BodyMeasurements.objects.get()
        self.assertEqual(body.email, 'test@example.com')
        self.assertEqual(float(BodyMeasurements.objects.get().height), 180.5)

    def test_create_body_measurements_invalid_data(self):
        """Test creating body measurements with invalid data"""
        response = self.client.post(
            self.body_measurements_url,
            self.invalid_measurements_data,
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(BodyMeasurements.objects.count(), 0)