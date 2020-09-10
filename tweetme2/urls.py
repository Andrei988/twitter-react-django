from django.contrib import admin
from django.urls import path, include

from tweets.views import (
    apiOverview, home_view, tweet_list_view, tweet_detail_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', apiOverview),
    path('', home_view),
    path('api/tweets/', include('tweets.urls'))
]
