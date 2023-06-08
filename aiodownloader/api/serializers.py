from rest_framework import serializers

class TikTokSerializer(serializers.Serializer):
    video_url = serializers.URLField()