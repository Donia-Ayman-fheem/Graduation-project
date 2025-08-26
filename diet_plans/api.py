from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import DietPlan, DietPlanWeek, DietPlanMeal
from .serializers import (
    DietPlanListSerializer,
    DietPlanDetailSerializer
)


class DietPlanListView(generics.ListAPIView):
    """
    API view to list all diet plans
    """
    queryset = DietPlan.objects.all()
    serializer_class = DietPlanListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Apply category filter if provided
        category = request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Diet plans retrieved successfully',
            'data': serializer.data
        })


class DietPlanDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific diet plan with all its details
    """
    queryset = DietPlan.objects.all()
    serializer_class = DietPlanDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': 'Diet plan details retrieved successfully',
            'data': serializer.data
        })
