from rest_framework import serializers, status, permissions, generics, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User 
from django.http import HttpResponse
import requests
import logging
import json

# Healthcheck for if system is up and functional
## Used for checking in docker-compose
def healthcheck(request):    
    return HttpResponse(request, status=200)

# Sample Action Logic + Response
## Receives an event via Hasura when an Action is triggered
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def action_sample(request):    
    req_body = json.loads(request.body)
    food = req_body['input']['food']
    if food == 'hotdog':
        response = { 'hotdog':'true' }
    else:
        response = { 'hotdog':'false' }
    return HttpResponse(json.dumps(response))