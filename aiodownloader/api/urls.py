from django.urls import path
from .views import TiktokDownload,homePage, YouTubeView, TiktokView

urlpatterns = [
     path('tik-tok/', TiktokView, name='tiktok'),
     path('', YouTubeView, name='youtube'),
     path('instagram/', homePage, name='homepage'),

     path('tiktok/', TiktokDownload.as_view(), name='tiktok'),
    #  path('insta/', InstaDownload.as_view(), name='instagram'),
]
