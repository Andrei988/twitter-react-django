
from django.contrib import admin
from django.urls import path, re_path # url()

from tweets.views import apiOverview, home_view, tweet_create_view, tweet_detail_view, tweet_list_view

urlpatterns = [
    path('', home_view),
    path('admin/', admin.site.urls),
    path('api/', apiOverview, name='api_overview'),
    path('create-tweet/', tweet_create_view, name='create-tweet'), 
    path('api/tweet-list/', tweet_list_view, name='tweet-list'),
    path('api/tweet/<int:pk>', tweet_detail_view, name='tweet-detail-view'),
]