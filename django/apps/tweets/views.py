
# Django is a web application framework for Python. It is designed to prioritize principles of reusability and rapid development.
# importing necessary library to connect between two platforms youtube Data API and twitter API. Twitter Top news topics are selected 
#to fetch details about those tweets and tried to feed the app with youtube videos based on the selected top news twitter topics. 
#Top 10 topics are wildfire, artificial inteligence, cryptocurrency,covid,immigration,inflation,lake mead. Rendering the output in localhost 



from multiprocessing import context
from django import http
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context
import tweepy
from django.http import JsonResponse
import pandas as pd
from django.shortcuts import render
from googleapiclient.discovery import build
from tweepy import OAuthHandler
from tweepy import Cursor
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from summer_proj_22.models import Tweets
from .serializers import TweetsSerializer

api_key = "
api_secret = "
access_token = ""
access_token_secret= ""
username= 
screen_name=username

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
user=api.verify_credentials()


class TweetsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Tweets.objects.all().order_by('retweet_count')
    
    serializer_class = TweetsSerializer
    permission_classes = [permissions.IsAuthenticated]

from datetime import datetime, timedelta
import pandas as pd


start_time = datetime(year=2020, month=10, day=1).strftime('%Y-%m-%dT%H:%M:%SZ')
end_time = datetime(year=2021, month=5, day=11).strftime('%Y-%m-%dT%H:%M:%SZ')

from googleapiclient.discovery import build
api_key = '' # Enter your own API key – this one won’t work

# Using Django web framework trying to fetch twitter data on topic stock market
def bbc(request):
        api_key = ''
        youtube = build('youtube', 'v3', developerKey=api_key)
        search_words = "stock market "
        date_since = "2018-11-16"
        context = {'tweets' : tweepy.Cursor(api.search_tweets,
             q=search_words,
             lang="en",
              since_id=date_since).items(5),'results':youtube.search().list(q="stock market ", part="snippet", type="video", order="viewCount",
                             maxResults=5).execute(),'video_statistics': youtube.videos().list(id =['WluvF8Tj5tc','chZp2U09Qa8'],
                                        part='statistics').execute()}
        return render(request,'example_app/hello.html',context)

          
# Using Django web framework trying to fetch twitter data  and youtube videos on topic Cryptocurrency

def news(request): 
# Collect tweets
    search_words = "cryptocurrency"
    
    date_since = "2018-11-16"
    for search_word in search_words:
        context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_word,
              lang="en",
              since_id=date_since).items(10)}
     
        return render(request,'example_app/news.html',context)

# Using Django web framework trying to fetch twitter data  and youtube videos on topic wildfire
def forest(request):
  
# Collect tweets
    search_words = "wildfire "
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(5),'results':youtube.search().list(q="stock market ", part="snippet", type="video", order="viewCount",
                             maxResults=5).execute()}
    return render(request,'example_app/news.html',context)
def cvd(request):
# Collect tweets
    search_words = "Covid"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_users,
              q=search_words,
              lang="en",
              since_id=date_since).items(5),'results':youtube.search().list(q="stock market ", part="snippet", type="video", order="viewCount",
                             maxResults=5).execute()}
    return render(request,'example_app/news.html',context)

def tech(request):
# Collect tweets
    search_words = "artificial intelligence"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(5),'results':youtube.search().list(q="stock market ", part="snippet", type="video", order="viewCount",
                             maxResults=5).execute()}
  
    return render(request,'example_app/news.html',context)

def img(request):
# Collect tweets
    search_words = "Immigration"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(5),'results':youtube.search().list(q="stock market ", part="snippet", type="video", order="viewCount",
                             maxResults=5).execute()}
  
    return render(request,'example_app/news.html',context)
def infl(request):
# Collect tweets
    search_words = "Inflation"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(5),'results':youtube.search().list(q="stock market ", part="snippet", type="video", order="viewCount",
                             maxResults=5).execute()}
  
    return render(request,'example_app/news.html',context)
def lake(request):
# Collect tweets
    search_words = "Lake mead"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(5),'results':youtube.search().list(q="stock market ", part="snippet", type="video", order="viewCount",
                             maxResults=5).execute()}
  
    return render(request,'example_app/news.html',context)
def c(request): 
# Collect tweets
    api_key = ''
    youtube = build('youtube', 'v3', developerKey=api_key)
    search_words = "#wildfires"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(2), 'results':youtube.search().list(q="wildfire ", part="snippet", type="video", order="viewCount",
                             maxResults=1).execute()}
   return render(request,'example_app/hello.html',context)

def youtube(request):
    youtube = build('youtube', 'v3', developerKey=api_key)

   # results = youtube.search().list(q="wildfire ", part="snippet", type="video", order="viewCount",
     #                        maxResults=10).execute()
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part="contentDetails",
        id="v=x-alwfgQ-cY&t=922s"
    )
    response = request.execute()
    print(response)
   return JsonResponse(response)

def tesla(request):
    youtube = build('youtube', 'v3', developerKey='')
    results2 = youtube.search().list(q="tesla ", part="snippet", type="video", order="viewCount",
    
                         maxResults=10).execute()
    #foos = results2.json['items']
    #for foo in foos:
      #  print(foo['snippet']['title'])
    return HttpResponse(results2)

def like(request):

    youtube = build('youtube', 'v3', developerKey='')
    
    context={'video_statistics': youtube.videos().list(id =['WluvF8Tj5tc','chZp2U09Qa8'],
                                        part='statistics').execute()}
  return render(request,'example_app/fire.html',context)








  


  





