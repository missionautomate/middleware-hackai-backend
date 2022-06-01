# myapi/urls.py
from django.urls import include, path
from . import views

urlpatterns = [ 
    path('login', views.google_login),
    path('add-user', views.new_user),
    path('get-img', views.galery_pull),
    path('add-image', views.add_image),
    path('remove-image', views.remove_image)
]