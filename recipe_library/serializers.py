from rest_framework import serializers
from .models import Recipe


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing recipes
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    total_time = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'category', 'category_display',
            'image', 'preparation_time', 'cooking_time', 'total_time',
            'calories', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_time(self, obj):
        """Calculate total time (prep + cooking)"""
        prep_time = obj.preparation_time or 0
        cook_time = obj.cooking_time or 0
        return prep_time + cook_time


class RecipeDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed recipe information
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    total_time = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'category', 'category_display',
            'ingredients', 'instructions', 'preparation_time', 'cooking_time',
            'total_time', 'servings', 'calories', 'protein', 'carbs', 'fat',
            'image', 'video_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total_time(self, obj):
        """Calculate total time (prep + cooking)"""
        prep_time = obj.preparation_time or 0
        cook_time = obj.cooking_time or 0
        return prep_time + cook_time
