# users/urls.py
from django.urls import path

from users.views import register

urlpatterns = [
    path('register/', register, name='register'),
    #path('', views.dashboard, name='dashboard'),

    # login logout
    #path('login/', login, name='login'),
    #path('logout/', logout, name='logout'),
    #path('logout-then-login/', logout_then_login, name='logout_then_login'),
]