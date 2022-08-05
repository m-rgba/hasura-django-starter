from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Tweets


class TweetsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweets
        fields = ['username', 'tweet_number', 'created_at', 'time']



