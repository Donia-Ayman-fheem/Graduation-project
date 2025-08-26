from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Recipe
from .serializers import RecipeListSerializer, RecipeDetailSerializer


class RecipeListView(generics.ListAPIView):
    """
    API view to list all recipes
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Apply category filter if provided
        category = request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
            
        # Apply search filter if provided
        search = request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(title__icontains=search)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Recipes retrieved successfully',
            'data': serializer.data
        })


class RecipeDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific recipe with all its details
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': 'Recipe details retrieved successfully',
            'data': serializer.data
        })
