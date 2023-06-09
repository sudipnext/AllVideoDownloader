from django.urls import path
from .views import TiktokDownload, InstaDownload, YouTubeView, TiktokView, YoutubeDownload, InstaGramView

urlpatterns = [
    #static serving urls
     path('tik-tok/', TiktokView, name='tk'),
     path('', YouTubeView, name='yt'),
     path('instagram/', InstaGramView, name='insta'),
     #api's
     path('tiktok/', TiktokDownload.as_view(), name='tiktok'),
     path('insta/', InstaDownload.as_view(), name='instagram'),
     path('ytb/', YoutubeDownload.as_view(), name='ytb'),

]
