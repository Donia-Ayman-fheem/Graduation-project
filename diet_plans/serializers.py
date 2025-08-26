from rest_framework import serializers
from .models import DietPlan, DietPlanWeek, DietPlanMeal


class DietPlanMealSerializer(serializers.ModelSerializer):
    """
    Serializer for the DietPlanMeal model
    """
    meal_type_display = serializers.CharField(source='get_meal_type_display', read_only=True)
    day_of_week_display = serializers.SerializerMethodField()

    class Meta:
        model = DietPlanMeal
        fields = [
            'id', 'meal_type', 'meal_type_display', 'day_of_week',
            'day_of_week_display', 'name', 'description', 'ingredients',
            'preparation', 'calories', 'protein', 'carbs', 'fat',
            'image', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_day_of_week_display(self, obj):
        days = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            7: 'Sunday'
        }
        return days.get(obj.day_of_week)


class DietPlanWeekSerializer(serializers.ModelSerializer):
    """
    Serializer for the DietPlanWeek model
    """
    meals = DietPlanMealSerializer(many=True, read_only=True)

    class Meta:
        model = DietPlanWeek
        fields = [
            'id', 'week_number', 'description', 'meals',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DietPlanListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing diet plans
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    weeks_count = serializers.SerializerMethodField()

    class Meta:
        model = DietPlan
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'duration_weeks', 'calories_per_day', 'protein_percentage',
            'carbs_percentage', 'fat_percentage', 'image',
            'weeks_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_weeks_count(self, obj):
        return obj.weeks.count()


class DietPlanDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed diet plan information
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    weeks = DietPlanWeekSerializer(many=True, read_only=True)

    class Meta:
        model = DietPlan
        fields = [
            'id', 'name', 'description', 'category', 'category_display',
            'duration_weeks', 'calories_per_day', 'protein_percentage',
            'carbs_percentage', 'fat_percentage', 'image',
            'weeks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
