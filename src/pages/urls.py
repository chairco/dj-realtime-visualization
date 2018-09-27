# pages/urls.py
from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth.decorators import login_required, permission_required

from pages.views import views


urlpatterns = [
    # blog(index's information)
    url(r'^(?P<pk>\d+)/$', views.BlogDetail.as_view(), name='blog_detail'),
    url(r'^add/$', login_required(views.BlogCreateView.as_view()), name='blog_add'),
    url(r'^(?P<pk>\d+)/edit/$', views.BlogUpdateView.as_view(), name='blog_edit'),
]


urlpatterns = format_suffix_patterns(urlpatterns)