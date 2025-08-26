from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import DietPlan, DietPlanWeek, DietPlanMeal


class DietPlanMealInline(admin.TabularInline):
    model = DietPlanMeal
    extra = 1
    fields = ('day_of_week', 'meal_type', 'name', 'calories')


class DietPlanWeekInline(admin.TabularInline):
    model = DietPlanWeek
    extra = 1
    fields = ('week_number', 'description')


@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'duration_weeks', 'calories_per_day', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DietPlanWeekInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'duration_weeks', 'image')
        }),
        (_('Nutritional Information'), {
            'fields': ('calories_per_day', 'protein_percentage', 'carbs_percentage', 'fat_percentage'),
            'classes': ('collapse',),
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(DietPlanWeek)
class DietPlanWeekAdmin(admin.ModelAdmin):
    list_display = ('diet_plan', 'week_number', 'created_at')
    list_filter = ('diet_plan', 'created_at')
    search_fields = ('diet_plan__name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DietPlanMealInline]


@admin.register(DietPlanMeal)
class DietPlanMealAdmin(admin.ModelAdmin):
    list_display = ('name', 'week', 'day_of_week', 'meal_type', 'calories')
    list_filter = ('meal_type', 'day_of_week', 'week__diet_plan', 'week')
    search_fields = ('name', 'description', 'ingredients')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('week', 'day_of_week', 'meal_type', 'name', 'description')
        }),
        (_('Details'), {
            'fields': ('ingredients', 'preparation', 'image')
        }),
        (_('Nutritional Information'), {
            'fields': ('calories', 'protein', 'carbs', 'fat'),
            'classes': ('collapse',),
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
