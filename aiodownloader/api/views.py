from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse,HttpResponseNotFound
from .serializers import *
from django.template import loader
import requests
import instaloader
import re
import os
from django.http import FileResponse
from django.conf import settings


def InstaGramView(request):
    template = loader.get_template('instagram.html')
    return HttpResponse(template.render())
def YouTubeView(request):
    template = loader.get_template('youtube.html')
    return HttpResponse(template.render())
def TiktokView(request):
    template = loader.get_template('tiktok.html')
    return HttpResponse(template.render())


# tiktok 
class TiktokDownload(APIView):
    def post(self, request):
        serializer = TikTokSerializer(data=request.data)
        if serializer.is_valid():
            video_url = serializer.validated_data['video_url']
            tiktokofficial = requests.get('https://www.tiktok.com/oembed/', params={'url': video_url})
            data = tiktokofficial.json()
            response = requests.get('https://www.cloudconversion.online/ssstik/', params={'video': video_url})
            response = response.json()
            description = data["title"]
            thumbnail_url = data["thumbnail_url"]
            response['description'] = description
            response['thumbnail_url'] = thumbnail_url
            return Response(response)
        return Response(serializer.errors, status=400)


# youtube 
class YoutubeDownload(APIView):
    def post(self, request):
        serializer = YoutubeSerializer(data=request.data)
        if serializer.is_valid():
            video_url = serializer.validated_data['video_url']
            response = requests.get('https://api.youtubemultidownloader.com/video', params={'url': video_url})
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    return Response(response_json)
                except ValueError:
                    return Response({'error': 'Invalid response from the YouTube API'}, status=500)
            else:
                return Response({'error': f'Failed to retrieve YouTube video information: {response.status_code}'}, status=500)
            
        return Response(serializer.errors, status=400)
  

class InstaDownload(APIView):
    def post(self, request):
        serializer = InstagramSerializer(data=request.data)
        if serializer.is_valid():
            video_url = serializer.validated_data['video_url']
            res = InstaDownloader(video_url)
            return Response(res, 200)
        
#downloads the file
def InstaDownloader(url):
    L = instaloader.Instaloader()
    shortcode = re.findall(r'/([A-Za-z0-9_-]+?)/?$', url)[0]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    target = 'downloads'
    L.download_post(post, target=target)
    description = post.caption.strip()
    filenames = []
    for filename in os.listdir(target):
        if filename.startswith(post.date_utc.strftime('%Y-%m-%d')):
            filenames.append(filename)
    # Rename the files to the shortcode
    for filename in filenames:
        old_path = os.path.join(target, filename)
        new_filename = f"{shortcode}{os.path.splitext(filename)[1]}"
        new_path = os.path.join(target, new_filename)
        os.rename(old_path, new_path)
    download_url = f"http://localhost:8000/media/videos/{shortcode}/"
    return {"description":description, "download_url": download_url}


def serve_video(request, video_code):
    video_filename = f"{video_code}.mp4"
    video_path = os.path.join(settings.BASE_DIR, 'downloads', video_filename)
    if os.path.exists(video_path):
        response = FileResponse(open(video_path, 'rb'), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{video_filename}"'
        return response
    else:
        return HttpResponseNotFound("File not found")