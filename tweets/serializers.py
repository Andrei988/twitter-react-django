from django.conf import settings
from rest_framework import serializers

from.models import Tweet
from rest_framework.fields import CurrentUserDefault

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

class TweetSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Tweet
        fields = ['content', 'user']

    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)