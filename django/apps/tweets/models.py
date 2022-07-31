from django.db import models

class tweets(models.Model): 
    user_id = models.CharField(max_length=64)
    twitter_id = models.CharField()