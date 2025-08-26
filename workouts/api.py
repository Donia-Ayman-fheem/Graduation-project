from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import (
    Exercise, WorkoutPlan, WorkoutDay, WorkoutExercise,
    UserWorkout, VideoTutorial, SavedVideo
)
from .serializers import (
    ExerciseSerializer,
    WorkoutPlanListSerializer,
    WorkoutPlanDetailSerializer,
    UserWorkoutSerializer,
    VideoTutorialSerializer,
    SavedVideoSerializer,
    SavedVideoCreateSerializer
)


class WorkoutPlanListView(generics.ListAPIView):
    """
    API view to list all workout plans
    """
    queryset = WorkoutPlan.objects.filter(is_active=True)
    serializer_class = WorkoutPlanListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Apply category filter if provided
        category = request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        # Apply difficulty filter if provided
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        # Apply featured filter if provided
        featured = request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Workout plans retrieved successfully',
            'data': serializer.data
        })


class WorkoutPlanDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific workout plan with all its details
    """
    queryset = WorkoutPlan.objects.filter(is_active=True)
    serializer_class = WorkoutPlanDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': 'Workout plan details retrieved successfully',
            'data': serializer.data
        })


class UserWorkoutListView(generics.ListCreateAPIView):
    """
    API view to list and create user workouts
    """
    serializer_class = UserWorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserWorkout.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Your workout plans retrieved successfully',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the workout plan exists and is active
        workout_plan_id = request.data.get('workout_plan_id')
        workout_plan = get_object_or_404(WorkoutPlan, id=workout_plan_id, is_active=True)

        # Create the user workout
        user_workout = UserWorkout.objects.create(
            user=request.user,
            workout_plan=workout_plan,
            notes=serializer.validated_data.get('notes', '')
        )

        # Update the user's profile to set this as their selected workout plan
        profile = request.user.profile
        profile.workout_plan = workout_plan
        profile.save()

        return Response({
            'message': f'You have successfully selected the "{workout_plan.name}" workout plan',
            'data': UserWorkoutSerializer(user_workout).data
        }, status=status.HTTP_201_CREATED)


class UserWorkoutDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a user workout
    """
    serializer_class = UserWorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserWorkout.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': 'Workout plan details retrieved successfully',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # If completed status changed to True, update the profile
        if 'completed' in request.data and request.data['completed']:
            profile = request.user.profile
            if profile.workout_plan and profile.workout_plan.id == instance.workout_plan.id:
                profile.workout_plan = None
                profile.save()

        return Response({
            'message': 'Workout plan updated successfully',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # If this is the selected workout plan in the profile, remove it
        profile = request.user.profile
        if profile.workout_plan and profile.workout_plan.id == instance.workout_plan.id:
            profile.workout_plan = None
            profile.save()

        self.perform_destroy(instance)
        return Response({
            'message': 'Workout plan removed successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class VideoTutorialListView(generics.ListAPIView):
    """
    API view to list video tutorials for a workout plan
    """
    serializer_class = VideoTutorialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        workout_plan_id = self.kwargs.get('workout_plan_id')
        return VideoTutorial.objects.filter(
            workout_plan_id=workout_plan_id,
            is_active=True
        ).order_by('order')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Apply featured filter if provided
        featured = request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Video tutorials retrieved successfully',
            'data': serializer.data
        })


class VideoTutorialDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific video tutorial
    """
    queryset = VideoTutorial.objects.filter(is_active=True)
    serializer_class = VideoTutorialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': 'Video tutorial details retrieved successfully',
            'data': serializer.data
        })


class SavedVideoListView(generics.ListCreateAPIView):
    """
    API view to list and create saved videos in the user's library
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'category']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = SavedVideo.objects.filter(user=self.request.user)

        # Filter by category if provided
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        # Filter by favorites if provided
        favorites = self.request.query_params.get('favorites', None)
        if favorites and favorites.lower() == 'true':
            queryset = queryset.filter(is_favorite=True)

        # Filter by source type if provided
        source_type = self.request.query_params.get('source_type', None)
        if source_type:
            queryset = queryset.filter(source_type=source_type)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SavedVideoCreateSerializer
        return SavedVideoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Your video library retrieved successfully',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Pass the request in the context
        serializer.context['request'] = request
        self.perform_create(serializer)

        return Response({
            'message': 'Video saved to your library successfully',
            'data': SavedVideoSerializer(serializer.instance).data
        }, status=status.HTTP_201_CREATED)


class SavedVideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a saved video
    """
    serializer_class = SavedVideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedVideo.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': 'Saved video details retrieved successfully',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Saved video updated successfully',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Video removed from your library successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class SaveVideoFromTutorialView(APIView):
    """
    API view to save a video tutorial to the user's library
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        tutorial_id = request.data.get('tutorial_id')

        if not tutorial_id:
            return Response({
                'error': 'Tutorial ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the tutorial
            tutorial = get_object_or_404(VideoTutorial, id=tutorial_id, is_active=True)

            # Check if already saved
            existing = SavedVideo.objects.filter(
                user=request.user,
                source_type='tutorial',
                source_id=tutorial_id
            ).first()

            if existing:
                return Response({
                    'message': 'This video is already in your library',
                    'data': SavedVideoSerializer(existing).data
                })

            # Save to library
            saved_video = SavedVideo.objects.create(
                user=request.user,
                title=tutorial.title,
                description=tutorial.description,
                video_url=tutorial.video_url,
                category='WO',  # Workout category
                duration_minutes=tutorial.duration_minutes,
                duration_seconds=tutorial.duration_seconds,
                thumbnail=tutorial.thumbnail,
                source_type='tutorial',
                source_id=tutorial_id
            )

            return Response({
                'message': 'Tutorial saved to your library successfully',
                'data': SavedVideoSerializer(saved_video).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ToggleFavoriteVideoView(APIView):
    """
    API view to toggle favorite status of a saved video
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            saved_video = get_object_or_404(SavedVideo, id=pk, user=request.user)
            saved_video.is_favorite = not saved_video.is_favorite
            saved_video.save()

            action = "added to" if saved_video.is_favorite else "removed from"

            return Response({
                'message': f'Video {action} favorites successfully',
                'data': SavedVideoSerializer(saved_video).data
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class WorkoutPlanSelectionView(APIView):
    """
    API view to select a workout plan for the user
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        workout_plan_id = request.data.get('workout_plan_id')

        if not workout_plan_id:
            return Response({
                'error': 'Workout plan ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the workout plan exists and is active
            workout_plan = get_object_or_404(WorkoutPlan, id=workout_plan_id, is_active=True)

            # Create or update user workout
            user_workout, created = UserWorkout.objects.get_or_create(
                user=request.user,
                workout_plan=workout_plan,
                defaults={'is_active': True}
            )

            if not created:
                user_workout.is_active = True
                user_workout.completed = False
                user_workout.save()

            # Update the user's profile
            profile = request.user.profile
            profile.workout_plan = workout_plan
            profile.save()

            return Response({
                'message': f'You have successfully selected the "{workout_plan.name}" workout plan',
                'data': UserWorkoutSerializer(user_workout).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
