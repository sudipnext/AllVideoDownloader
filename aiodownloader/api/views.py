from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TikTokSerializer
import requests

class TiktokDownload(APIView):
    def post(self, request):
        serializer = TikTokSerializer(data=request.data)
        if serializer.is_valid():
            video_url = serializer.validated_data['video_url']
            response = requests.get('https://www.cloudconversion.online/ssstik/', params={'video': video_url})
            response = response.json()
            return Response(response)
        return Response(serializer.errors, status=400)
