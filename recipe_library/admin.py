from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'preparation_time', 'cooking_time', 'calories', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'ingredients', 'instructions')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'image', 'video_url')
        }),
        (_('Recipe Details'), {
            'fields': ('ingredients', 'instructions', 'preparation_time', 'cooking_time', 'servings')
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
