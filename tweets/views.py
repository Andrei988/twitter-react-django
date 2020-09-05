import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer

from rest_framework.fields import CurrentUserDefault
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import request

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Home view' : '/',
        'Admin page' : '/admin/',
        'Create tweet' : '/create-tweet/',
        'Tweets by id' : '/tweets/<int:tweet_id>/',
    }

    return Response(api_urls)

@api_view(['GET'])
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context = {}, status = 200)
    
@api_view(['POST'])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST or None)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
        return JsonResponse({}, status=400)
    try:
        pass
    except Exception as e:
            print(str(e))
            return JsonResponse({}, status=400, safe=False)
    return JsonResponse({}, status=201)

@api_view(['POST'])
def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if(request.headers.get("X-Requested-With") == "XMLHttpRequest"):
                return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form =  TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        print("object saved")
        if(request.headers.get("X-Requested-With") == "XMLHttpRequest"):
            return JsonResponse(obj.serialize(), status=201)

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
             return redirect(next_url) 
        form = TweetForm()

        if form.errors:
            if(request.headers.get("X-Requested-With") == "XMLHttpRequest"):
                return JsonResponse(form.errors, status=400)

    else:
        print(form.errors)
    return render(request, 'components/form.html', context={"form" : form})
    
@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    tweets = Tweet.objects.all()
    serializer = TweetSerializer(tweets, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def tweet_detail_view(request, pk, *args, **kwargs):
    tweet = Tweet.objects.get(id=pk);
    serializer = TweetSerializer(tweet, many=False)

    return Response(serializer.data)
