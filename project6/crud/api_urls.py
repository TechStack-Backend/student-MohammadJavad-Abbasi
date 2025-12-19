from django.urls import path
from .api_views import DeveloperListAPIView

urlpatterns = [
    path('developers/', DeveloperListAPIView.as_view(), name='api-developers'),
]
