from django.db import models

class GoogleUser(models.Model):
    googleId = models.CharField(max_length=30)
    imageUrl = models.URLField(max_length=200)
    name = models.CharField(max_length=60)
    email = models.EmailField()
    givenName = models.CharField(max_length=60)
    familyName = models.CharField(max_length=60)
    def __str__(self):
        return self.name