from django.urls import path, include
from . import api

app_name = 'additional_forms'

# API URL patterns
api_urlpatterns = [
    path('contact/', api.ContactFormCreateView.as_view(), name='contact_form'),
    path('subscribe/', api.SubscriptionCreateView.as_view(), name='subscription'),
    path('body-measurements/', api.BodyMeasurementsCreateView.as_view(),
         name='body_measurements'),
]

urlpatterns = [
    # API endpoints
    path('api/', include((api_urlpatterns, 'api'))),
]
