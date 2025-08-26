from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Profile, Gender, FitnessGoal

User = get_user_model()

class AccountsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:api:register')
        self.login_url = reverse('accounts:api:token_obtain_pair')
        self.profile_url = reverse('accounts:api:profile')
        self.change_password_url = reverse('accounts:api:change_password')

        # Test user data
        self.user_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        }

        # Create a test user for login tests
        self.test_user = User.objects.create_user(
            email='existing@example.com',
            name='Existing User',
            password='ExistingPassword123!'
        )
        Profile.objects.create(user=self.test_user)

    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Check if user was created in database
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())

        # Check if profile was created
        user = User.objects.get(email=self.user_data['email'])
        self.assertTrue(hasattr(user, 'profile'))

    def test_user_login(self):
        """Test user login endpoint"""
        login_data = {
            'email': 'existing@example.com',
            'password': 'ExistingPassword123!'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_profile(self):
        """Test getting user profile"""
        # Authenticate
        self.client.force_authenticate(user=self.test_user)

        # Get profile
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.test_user.email)
        self.assertEqual(response.data['name'], self.test_user.name)
        self.assertIn('profile', response.data)

    def test_update_profile(self):
        """Test updating user profile"""
        # Authenticate
        self.client.force_authenticate(user=self.test_user)

        # Update data
        update_data = {
            'name': 'Updated Name',
            'profile': {
                'age': 30,
                'gender': Gender.MALE,
                'fitness_goal': FitnessGoal.WEIGHT_LOSS
            }
        }

        # Update profile
        response = self.client.patch(self.profile_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh from database
        self.test_user.refresh_from_db()
        self.test_user.profile.refresh_from_db()

        # Check if updated
        self.assertEqual(self.test_user.name, 'Updated Name')
        self.assertEqual(self.test_user.profile.age, 30)
        self.assertEqual(self.test_user.profile.gender, Gender.MALE)
        self.assertEqual(self.test_user.profile.fitness_goal, FitnessGoal.WEIGHT_LOSS)

    def test_change_password(self):
        """Test changing password"""
        # Authenticate
        self.client.force_authenticate(user=self.test_user)

        # Password data
        password_data = {
            'old_password': 'ExistingPassword123!',
            'new_password': 'NewStrongPassword456!',
            'confirm_password': 'NewStrongPassword456!'
        }

        # Change password
        response = self.client.put(self.change_password_url, password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Check if password was changed
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.check_password('NewStrongPassword456!'))

    def test_update_body_measurements(self):
        """Test updating body measurements"""
        # Authenticate
        self.client.force_authenticate(user=self.test_user)

        # URL for body measurements
        body_measurements_url = reverse('accounts:api:body_measurements')

        # Body measurements data
        measurements_data = {
            'height': 180.5,
            'weight': 75.2,
            'waist_circumference': 85.0,
            'hip_circumference': 95.0,
            'chest_circumference': 100.0,
            'arm_circumference': 35.0,
            'thigh_circumference': 55.0,
            'neck_circumference': 40.0
        }

        # Update body measurements
        response = self.client.patch(body_measurements_url, measurements_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)

        # Refresh from database
        self.test_user.profile.refresh_from_db()

        # Check if measurements were updated
        self.assertEqual(float(self.test_user.profile.height), 180.5)
        self.assertEqual(float(self.test_user.profile.weight), 75.2)
        self.assertEqual(float(self.test_user.profile.waist_circumference), 85.0)
        self.assertEqual(float(self.test_user.profile.hip_circumference), 95.0)
        self.assertEqual(float(self.test_user.profile.chest_circumference), 100.0)
        self.assertEqual(float(self.test_user.profile.arm_circumference), 35.0)
        self.assertEqual(float(self.test_user.profile.thigh_circumference), 55.0)
        self.assertEqual(float(self.test_user.profile.neck_circumference), 40.0)
