# myapi/urls.py
from django.urls import include, path
from . import views

urlpatterns = [ 
    path('login', views.google_login),
    path('addUser', views.new_user),
    path('getImg', views.galery_pull)
]