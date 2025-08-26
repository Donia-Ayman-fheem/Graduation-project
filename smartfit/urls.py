from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('forms/', include('additional_forms.urls')),
    path('diet-plans/', include('diet_plans.urls')),
    path('recipes/', include('recipe_library.urls')),
    path('shop/', include('shopping.urls')),
    path('workouts/', include('workouts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add debug toolbar in development
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
