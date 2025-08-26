from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from . import api

app_name = 'accounts'

# API URL patterns
api_urlpatterns = [
    # Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', api.RegisterView.as_view(), name='register'),
    path('logout/', api.LogoutView.as_view(), name='logout'),

    # User profile endpoints
    path('profile/', api.UserProfileView.as_view(), name='profile'),
    path('change-password/', api.ChangePasswordView.as_view(), name='change_password'),
    path('body-measurements/', api.BodyMeasurementsUpdateView.as_view(), name='body_measurements'),
    path('select-diet-plan/', api.DietPlanSelectionView.as_view(), name='select_diet_plan'),
]

urlpatterns = [
    # Web views
    path('', views.home, name='home'),
    path('body-measurements/', views.body_measurements, name='body_measurements'),

    # API endpoints
    path('api/', include((api_urlpatterns, 'api'))),
]
