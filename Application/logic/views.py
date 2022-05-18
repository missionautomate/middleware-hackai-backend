from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .serializers import GoogleUserSerializer
from .models import GoogleUser
from .test_db import get_gallery, add_user

import requests


class GoogleUserViewSet(viewsets.ModelViewSet):
    queryset = GoogleUser.objects.all().order_by('name')
    serializer_class = GoogleUserSerializer

@api_view(['POST'])
def google_login(request):
    if request.method == 'POST':
        received_data = JSONParser().parse(request)
        token = received_data[0]
        google_login_data = received_data[1]
        google_login_data_serializer = GoogleUserSerializer(data=google_login_data)

        oauth_url = 'https://oauth2.googleapis.com/tokeninfo'
        token_obj = {'access_token': token}

        oauth_request = requests.post(oauth_url, data=token_obj)

        # if google_login_data_serializer.is_valid():
        #     google_login_data_serializer.save()

        if(oauth_request.status_code == 200):
            add_user(received_data[1])
            return(HttpResponse(status=200))
        else:
            return(HttpResponse(status=401))

@api_view(['POST'])
def galery_pull(request):
    if request.method == 'POST':
        received_data = JSONParser().parse(request)
        google_id = received_data[0]
        data = get_gallery(google_id)
        if(data):
            return(data)
        else:
            return(HttpResponse(status=204))

@api_view(['POST'])
def new_user(request):
    if request.method == 'POST':
        received_data = JSONParser().parse(request)
        add_user(received_data)
        return(HttpResponse(status=200))