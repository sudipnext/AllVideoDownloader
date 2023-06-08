from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import *
from django.template import loader
import requests
import instaloader
import re

def InstaDownloader(url):
    L = instaloader.Instaloader()
    shortcode = re.findall(r'/([A-Za-z0-9_-]+?)/?$', url)[0]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    target = 'downloads/'
    L.download_post(post, target=target)


def homePage(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
def YouTubeView(request):
    template = loader.get_template('youtube.html')
    return HttpResponse(template.render())
def TiktokView(request):
    template = loader.get_template('tiktok.html')
    return HttpResponse(template.render())

class TiktokDownload(APIView):
    def post(self, request):
        serializer = TikTokSerializer(data=request.data)
        if serializer.is_valid():
            video_url = serializer.validated_data['video_url']
            response = requests.get('https://www.cloudconversion.online/ssstik/', params={'video': video_url})
            response = response.json()
            return Response(response)
        return Response(serializer.errors, status=400)

class InstaDownload(APIView):
    def post(self, request):
        serializer = InstagramSerializer(data=request.data)
        if serializer.is_valid():
            video_url = serializer.validated_data['video_url']
            InstaDownloader(video_url)
            return Response({"tarun": "gill"}, 200)
