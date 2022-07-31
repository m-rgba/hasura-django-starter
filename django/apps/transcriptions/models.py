from django.db import models
from sympy import content

class transcriptions(models.Model): 
    video_id = models.CharField(max_length=64)
    title = models.CharField()
    descriptions = models.CharField()
    content = models.CharField()