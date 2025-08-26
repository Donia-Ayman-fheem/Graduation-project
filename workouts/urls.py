from django.urls import path, include
from . import api

app_name = 'workouts'

# API URL patterns
api_urlpatterns = [
    # Workout plan endpoints
    path('plans/', api.WorkoutPlanListView.as_view(), name='plan_list'),
    path('plans/<int:pk>/', api.WorkoutPlanDetailView.as_view(), name='plan_detail'),

    # User workout endpoints
    path('my-workouts/', api.UserWorkoutListView.as_view(), name='user_workout_list'),
    path('my-workouts/<int:pk>/', api.UserWorkoutDetailView.as_view(), name='user_workout_detail'),

    # Workout plan selection endpoint
    path('select-plan/', api.WorkoutPlanSelectionView.as_view(), name='select_plan'),

    # Video tutorial endpoints
    path('plans/<int:workout_plan_id>/videos/', api.VideoTutorialListView.as_view(), name='video_list'),
    path('videos/<int:pk>/', api.VideoTutorialDetailView.as_view(), name='video_detail'),

    # Video library endpoints
    path('video-library/', api.SavedVideoListView.as_view(), name='video_library'),
    path('video-library/<int:pk>/', api.SavedVideoDetailView.as_view(), name='saved_video_detail'),
    path('video-library/save-tutorial/', api.SaveVideoFromTutorialView.as_view(), name='save_tutorial'),
    path('video-library/<int:pk>/toggle-favorite/', api.ToggleFavoriteVideoView.as_view(), name='toggle_favorite'),
]

urlpatterns = [
    # API endpoints
    path('api/', include((api_urlpatterns, 'api'))),
]
