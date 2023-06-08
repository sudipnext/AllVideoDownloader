from django.urls import path
from .views import TiktokDownload

urlpatterns = [
    path('tiktok/', TiktokDownload.as_view(), name='tiktok'),
]
