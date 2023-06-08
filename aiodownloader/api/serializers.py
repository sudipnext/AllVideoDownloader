from rest_framework import serializers

class TikTokSerializer(serializers.Serializer):
    video_url = serializers.URLField()

class InstagramSerializer(serializers.Serializer):
    video_url = serializers.URLField()

class YoutubeSerializer(serializers.Serializer):
    video_url = serializers.URLField()