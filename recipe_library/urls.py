from django.urls import path, include
from . import api

app_name = 'recipe_library'

# API URL patterns
api_urlpatterns = [
    path('', api.RecipeListView.as_view(), name='list'),
    path('<int:pk>/', api.RecipeDetailView.as_view(), name='detail'),
]

urlpatterns = [
    # API endpoints
    path('api/', include((api_urlpatterns, 'api'))),
]
