from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse,HttpResponseNotFound
from .serializers import *
from django.template import loader
import requests
import instaloader
import re
import time
import os
from django.http import FileResponse
from django.conf import settings
from django.urls import resolve
from mechanicalsoup import StatefulBrowser



#Static file views
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
            description = data["author_name"]
            thumbnail_url = data["thumbnail_url"]
            response['description'] = description +"/"+ data["embed_product_id"]
            response['thumbnail_url'] = thumbnail_url
            return Response(response)
        return Response(serializer.errors, status=400)


class YoutubeDownload(APIView):
    def post(self, request):
        serializer = YoutubeSerializer(data=request.data)
        if serializer.is_valid():
            video_url = serializer.validated_data['video_url']
            try:
                response = requests.get(f'https://api.youtubemultidownloader.com/video?url={video_url}')
                response_data = response.json()
                return Response(response_data)
            except requests.exceptions.RequestException as e:
                return Response({'error': 'Request error occurred'})
            except ValueError as e:
                return Response({'error': 'Error parsing JSON response'})
        else:
            return Response(serializer.errors)


class InstaDownload(APIView):
    def post(self, request):
        serializer = InstagramSerializer(data=request.data)
        if serializer.is_valid():
            video_url = serializer.validated_data['video_url']
            browser = StatefulBrowser()
            url = "https://downloadgram.org/"  # Replace with your actual URL
            browser.open(url)
            browser.select_form()
            url_input_name = "url"  # Replace with the actual name of the input field
            url_value = video_url  # Replace with the desired URL
            browser[url_input_name] = url_value
            browser.submit_selected()
            response = browser.get_current_page()
            video_element = response.find("video", class_="control-video")

            if video_element:
                video_url = video_element.source["src"]
                return Response({"download_url":video_url})
            else:
                print("Video element not found on the page.")

