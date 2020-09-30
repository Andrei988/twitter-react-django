from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from tweets.views import (
    apiOverview, home_view,
)
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('token-auth/', obtain_jwt_token),
    path('core/', include('core.urls')),
    path('react/', TemplateView.as_view(template_name='react/react.html')),
    path('admin/', admin.site.urls),
    path('api/', apiOverview),
    path('', home_view),
    path('api/tweets/', include('tweets.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
