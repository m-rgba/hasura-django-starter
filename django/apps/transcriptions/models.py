from django.db import models
from sympy import content

class transcriptions(models.Model): 
    video_id = models.TextField(max_length=64)
    title = models.TextField()
    descriptions = models.TextField()
    content = models.TextField()