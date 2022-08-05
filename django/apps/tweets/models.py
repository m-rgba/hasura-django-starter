from django.db import models
# Create your models here.

class Tweets(models.Model):
    username= models.TextField()
    tweet_number = models.IntegerField()
    created_at = models.IntegerField()
    time = models.IntegerField()
    retweet_count= models.IntegerField()
   
    

    def __str__(self):

        return self.tweet_number
