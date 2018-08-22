"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url

from pages.views.views import index
from pages.views import views

from films.api.v1 import api_views

from rest_framework import routers

from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='API')

v1 = routers.DefaultRouter()
v1.register(r'films', api_views.FilmViewSet)
v1.register(r'gaps', api_views.FilmGapViewSet)
v1.register(r'lens', api_views.FilmLenViewSet)

urlpatterns = [
    # App url
    path('', index, name='index'),
    path('films/', include('films.urls')),
    #path('pages/', include('pages.urls')),

    # Build-in url
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    # API url
    path('api/v1/', include(v1.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Docs url
    path('docs/', schema_view)
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
