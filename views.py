



from multiprocessing import context
from django import http
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
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
api_key = "CgyLDOJ4EuCh7O1X1StyqpPlE"
api_secret = "ENn0mOfSNHoLgtap7i9zPpH6RauVYRg2ytFs7hyqPVLHd9uwuw"
access_token = "1547609471387439108-po4gNeBavDZuq18uvbO7NsSnb4EqEP"
access_token_secret= "6OCZv7c3475qd5tWq0P3U6k8Z1KWk21aKM1E60mN3yc9f"
username= "SangeethaDG21"
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
api_key = 'AIzaSyBfoGn0960ZupAD7YiIdwfRe1MDbdg9F_U' # Enter your own API key – this one won’t work

def bbc(request):
         search_words = "stock market "
         date_since = "2018-11-16"
         context = {'tweets' : tweepy.Cursor(api.search_tweets,
             q=search_words,
             lang="en",
              since_id=date_since).items(10)}

         return render(request,'example_app/news.html',context)
        

#def bbc(request):
 #   words = ["market" , "wild fire"]
  #  date_since = "2018-11-16"
   # context_dict = {}
    #for word in words:
     #   context = {'tweets' : tweepy.Cursor(api.search_tweets,
      #       q=word,
       #     lang="en",
        #     since_id=date_since).items(10)}
        #context_dicts = context
        #for context_dict in context_dicts:
         #   print(context_dict)
          #  return render(request,'example_app/news.html',context_dict)

          


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


def forest(request):
  
# Collect tweets
    search_words = "wildfire "
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(100)}
  
    return render(request,'example_app/news.html',context)


def cvd(request):
# Collect tweets
    search_words = "Covid"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_users,
              q=search_words,
              lang="en",
              since_id=date_since).items(5)}
    return render(request,'example_app/news.html',context)

def tech(request):
 
  
# Collect tweets
    search_words = "artificial intelligence"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(5)}
  
    return render(request,'example_app/news.html',context)

def img(request):
 
  
# Collect tweets
    search_words = "Immigration"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(5)}
  
    return render(request,'example_app/news.html',context)


def infl(request):
 
  
# Collect tweets
    search_words = "Inflation"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(5)}
  
    return render(request,'example_app/news.html',context)

def lake(request):
 
  
# Collect tweets
    search_words = "Lake mead"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(5)}
  
    return render(request,'example_app/news.html',context)

def life(request):
 
  
# Collect tweets
    search_words = "Utopia"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(5)}
  
    return render(request,'example_app/news.html',context)




def c(request): 
# Collect tweets
    api_key = 'AIzaSyBfoGn0960ZupAD7YiIdwfRe1MDbdg9F_U'
    youtube = build('youtube', 'v3', developerKey=api_key)
    search_words = "#wildfires"
    date_since = "2018-11-16"
    context = {'tweets' : tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since_id=date_since).items(2), 'results':youtube.search().list(q="wildfire ", part="snippet", type="video", order="viewCount",
                             maxResults=1).execute()}
    
   # request = youtube.videos().list(
   #     part="contentDetails",
    #    id="v=x-alwfgQ-cY&t=922s"
   # )
    #response = request.execute()
   # print(response)
    video_ids=[]
   # rs=results['items']
    #for r in rs:
     #  print(r['kind'])
      # print(r['id']['videoId'])
      # print(r['contentDetails']['message'])
       
    
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
    youtube = build('youtube', 'v3', developerKey='AIzaSyBfoGn0960ZupAD7YiIdwfRe1MDbdg9F_U')
    results2 = youtube.search().list(q="tesla ", part="snippet", type="video", order="viewCount",
    
                         maxResults=10).execute()
    #foos = results2.json['items']
    #for foo in foos:
      #  print(foo['snippet']['title'])
    return HttpResponse(results2)

from youtube_transcript_api import YouTubeTranscriptApi
def kar(request):
     youtube = build('youtube', 'v3', developerKey='AIzaSyBfoGn0960ZupAD7YiIdwfRe1MDbdg9F_U')
     results3 = youtube.videos().list(id='geW09OOqieU',part="contentDetails").execute()
     
  
     print(results3)
     return HttpResponse(results3)








  


  




