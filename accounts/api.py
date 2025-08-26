from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from diet_plans.models import DietPlan
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    BodyMeasurementsUpdateSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return updated user data
        return Response(UserSerializer(user).data)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": ["Wrong password."]},
                            status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        # Generate new tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Password updated successfully',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            # Add the token to the blacklist
            token.blacklist()

            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class BodyMeasurementsUpdateView(generics.UpdateAPIView):
    """
    API view to update user's body measurements
    """
    serializer_class = BodyMeasurementsUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return updated user data with profile
        return Response({
            'message': ('Your body measurements have been updated successfully. '
                        'These measurements will help us create a personalized '
                        'fitness plan for you.'),
            'user': UserSerializer(request.user).data
        }, status=status.HTTP_200_OK)


class DietPlanSelectionView(generics.UpdateAPIView):
    """
    API view to select a diet plan for the user
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        diet_plan_id = request.data.get('diet_plan_id')

        if not diet_plan_id:
            return Response({
                'error': 'Diet plan ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            diet_plan = get_object_or_404(DietPlan, id=diet_plan_id)
            profile.diet_plan = diet_plan
            profile.save()

            return Response({
                'message': f'You have successfully selected the "{diet_plan.name}" diet plan.',
                'user': UserSerializer(request.user).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
