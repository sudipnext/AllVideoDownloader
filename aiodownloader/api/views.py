from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import *
from django.template import loader
import requests
from mechanicalsoup import StatefulBrowser
from bs4 import BeautifulSoup



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
            browser = StatefulBrowser()
            url = "https://vidiget.com/youtube-downloader-zp31r"
            response = browser.open(url)
            if response.ok:
                form = browser.select_form('.downloadform')
                form.set("youtube_video_page", video_url)  # Use the provided video_url
                response = browser.submit_selected()
                page_content = response.text
                soup = BeautifulSoup(page_content, 'html.parser')
                img_element = soup.find('img', {'class': 'img-thumbnail'})
                src = img_element['src']
                title = img_element['title']  # Extract the title attribute
                rows = soup.select('.table.files-table tbody tr')
                data = []
                for row in rows:
                    quality = row.select_one('td:nth-child(1)').text
                    file_type = row.select_one('td:nth-child(2)').text
                    fps_element = row.select_one('td.d-none.d-sm-table-cell:nth-child(3)')
                    fps = fps_element.text if fps_element else None
                    file_size_element = row.select_one('td.d-none.d-sm-table-cell:nth-child(4)')
                    file_size = file_size_element.text if file_size_element else None
                    download_link = row.select_one('td a')['href']
                    
                    # Exclude objects with "Download link" value of "javascript:void(0)"
                    if download_link != "javascript:void(0)":
                        row_data = {
                            'Quality': quality,
                            'Type': file_type,
                            'Fps': fps,
                            'File size': file_size,
                            'Downloadlink': download_link
                        }
                        data.append(row_data)
                
                response_data = {
                    'src': src,
                    'title': title,
                    'data': data,
                    'mp3': mp3Download(video_url)
                }    
                
                return Response(response_data)
            else:
                return Response({"error": "Failed to open the URL."})
        else:
            return Response(serializer.errors)

def mp3Download(video_url):
    browser = StatefulBrowser()
    url = "https://getn.topsandtees.space/s/zPrGJZxVON"
    browser.open(url)
    form = browser.select_form('#search_form')
    form.set("q", video_url)
    browser.submit_selected()
    page_content = browser.page
    download_link = page_content.find('a', class_='search-item__download')
    url = download_link['data-url']
    url = f"https://getn.topsandtees.space{url}/mp3"
    browser.open(url)
    updated_page_content = browser.page
    span = updated_page_content.find('span', class_='search-item__download')
    data_href = span['data-href']
    return data_href

#instagram
class InstaDownload(APIView):
    def post(self, request):
        serializer = InstagramSerializer(data=request.data)
        if serializer.is_valid():
            video_url = serializer.validated_data['video_url']
            browser = StatefulBrowser()
            url = "https://downloadgram.org/"  
            browser.open(url)
            browser.select_form()
            url_input_name = "url"  
            url_value = video_url  
            browser[url_input_name] = url_value
            browser.submit_selected()
            response = browser.get_current_page()
            video_element = response.find("video", class_="control-video")
            if response.ok:
                form = browser.select_form('.downloadform')
                form.set("youtube_video_page", "https://youtu.be/Qw3wbnzzyD4")


            if video_element:
                video_url = video_element.source["src"]
                return Response({"download_url":video_url})
            else:
                print("Video element not found on the page.")

