from django.urls import path, include
from . import api

app_name = 'diet_plans'

# API URL patterns
api_urlpatterns = [
    path('', api.DietPlanListView.as_view(), name='list'),
    path('<int:pk>/', api.DietPlanDetailView.as_view(), name='detail'),
]

urlpatterns = [
    # API endpoints
    path('api/', include((api_urlpatterns, 'api'))),
]
