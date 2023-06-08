from django.urls import path
from .views import TiktokDownload,homePage

urlpatterns = [
     path('', homePage, name='homepage'),
     path('tik-tok/', homePage, name='homepage'),
     path('instagram/', homePage, name='homepage'),
    path('tiktok/', TiktokDownload.as_view(), name='tiktok'),
]
