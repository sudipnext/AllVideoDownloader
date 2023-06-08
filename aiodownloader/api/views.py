from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import *
from django.template import loader
import requests
import instaloader
import html
import re
from bs4 import BeautifulSoup


def homePage(request):
    template = loader.get_template('index.html')
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
            response = requests.get('https://www.cloudconversion.online/ssstik/', params={'video': video_url})
            response = response.json()
            description = get_description(video_url)
            response['description'] = description
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
            InstaDownloader(video_url)
            return Response({"tarun": "gill"}, 200)
        

def InstaDownloader(url):
    L = instaloader.Instaloader()
    shortcode = re.findall(r'/([A-Za-z0-9_-]+?)/?$', url)[0]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    target = 'downloads/'
    L.download_post(post, target=target)


# tiktok_description_fetching for tiktok
def get_description(url):
    web_response = requests.get(url)
    soup = BeautifulSoup(web_response.content, "html.parser")
    meta_tag = soup.find('meta', attrs={'name': 'description'})

    if meta_tag is not None:
        content_value = meta_tag['content']
        decoded_value = html.unescape(content_value)
        start_text = '&quot;'
        end_text = '&quot;.'
        start_index = decoded_value.find(start_text) + len(start_text)
        end_index = decoded_value.find(end_text)
        desired_text = decoded_value[start_index:end_index]
        pattern = r'TikTok video from (.+?): "(.+)"\.'
        matches = re.search(pattern, desired_text)
        return matches.group(2)
    else:
        return "No matching meta tag found."
