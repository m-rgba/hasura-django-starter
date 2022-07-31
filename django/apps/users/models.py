from django.db import models

class users(models.Model): 
    user_id = models.CharField(max_length=64)
    twitter_id = models.CharField()
    descriptions = models.CharField()
    content = models.CharField()