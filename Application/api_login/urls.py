# myapi/urls.py
from django.urls import include, path
from . import views

urlpatterns = [ 
    path('login', views.google_login)
]