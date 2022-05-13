from rest_framework import serializers
from .models import GoogleUser

class GoogleUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoogleUser
        fields = ('id', 'googleId', 'imageUrl', 'name', 'email', 'givenName', 'familyName')