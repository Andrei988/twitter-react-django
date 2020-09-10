from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from tweets.forms import TweetForm
from tweets.models import Tweet, Like
from tweets.serializers import (
    TweetSerializer,
    TweetCreateSerializer,
    TweetActionSerializer)

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Home view': '/',
        'Admin page': '/admin/',
        'Create tweet': '/create-tweet/',
        'Tweets by id': '/tweets/<int:tweet_id>/',
    }

    return Response(api_urls)


@api_view(['GET'])
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    context = {
        "request": request
    }
    serializer = TweetCreateSerializer(data=request.POST, context=context)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def tweet_detail_view(request, pk, *args, **kwargs):
    qs = Tweet.objects.get(id=pk)
    if qs is None:
        return Response({}, status=404)
    serializer = TweetSerializer(qs)
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, pk, *args, **kwargs):
    try:
        qs = Tweet.objects.get(id=pk)
    except Exception as e:
        return Response(str(e), status=500)
    if qs is None:
        return Response({}, status=404)
    qs = Tweet.objects.all().filter(id=pk, user=request.user)
    if not qs:
        return Response({"message": "You cannot delete this tweet"}, status=401)
    Tweet.objects.get(id=pk).delete()
    return Response({"message": "Tweet removed"}, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):  # like, unlike, re-tweet

    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        obj = Tweet.objects.get(id=tweet_id)
        if action == 'like':
            obj.likes.add(request.user)
            like = Like()
            like.user = request.user
            like.tweet = obj
            like.save()
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'unlike':
            obj.likes.remove(request.user)
            likes = Like.objects.all()
            likes = likes.filter(user_id=request.user.id)
            likes = likes.filter(tweet_id=obj.id)
            likes.delete()
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'retweet':
            parent_obj = obj
            new_tweet = Tweet.objects.create(user=request.user, parent=parent_obj, content=content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        print("object saved")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(obj.serialize(), status=201)

        if next_url is not None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()

        if form.errors:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(form.errors, status=400)

    else:
        print(form.errors)
    return render(request, 'components/form.html', context={"form": form})
