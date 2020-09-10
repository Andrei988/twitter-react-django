from django.conf import settings
from rest_framework import serializers

from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS


class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if value not in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for a tweet.")
        return value

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class TweetCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = '__all__'

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, content):
        if len(content) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return content


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = '__all__'

    def get_likes(self, obj):
        return obj.likes.count()
