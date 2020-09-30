

from django.urls import path
from django.views.generic import TemplateView

from .views import (
    tweet_action_view,
    tweet_create_view,
    tweet_detail_view,
    tweet_delete_view,
    tweet_list_view,
)

urlpatterns = [
    path('react/', TemplateView.as_view(template_name='react/react.html')),
    path('', tweet_list_view),
    path('action/', tweet_action_view, name='tweet-action'),
    path('create/', tweet_create_view, name='create-tweet'),
    path('<int:pk>/', tweet_detail_view, name='tweet-detail-view'),
    path('<int:pk>/delete/', tweet_delete_view, name='tweet-delete-view')
]


