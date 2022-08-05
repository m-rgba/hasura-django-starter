from django.db import models


class summarizations(models.Model): 
    video_id = models.CharField(max_length=12)
    summary = models.CharField()
