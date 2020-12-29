from rest_framework import serializers, status, permissions, generics, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User 
from api.models import profile
from django.db import connection
from django.http import HttpResponse
from collections import namedtuple
import requests
import logging
import json

# Email > New Registration
## Uses Django ORM to update registration sent flag
@api_view(['POST'])
@permission_classes([AllowAny])
def new_registration_email(request):    
    req_body = json.loads(request.body)
    user_id = req_body['event']['data']['new']['id']
    email = req_body['event']['data']['new']['email']
    user = User.objects.get(id=user_id)
    registration_sent = user.profile.registration_sent
    if ( registration_sent == False ):        
        # TODO: --EMAIL LOGIC GOES HERE-- Boilerplate to send new registration email:
        # Update user to registration sent status
        user.profile.registration_sent = True
        user.save()
        return HttpResponse('Registration email sent.')
    else:
        return HttpResponse('Registration email already sent.')
    
# Email > Password Reset
## Uses SQL to update password reset sent flag
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_email(request):    
    req_body = json.loads(request.body)
    user_id = req_body['event']['data']['new']['user_id']
    token = req_body['event']['data']['new']['key']
    user = User.objects.get(id=user_id)
    email = user.email
    # Check status
    with connection.cursor() as cursor:
        cursor.execute("SELECT reset_sent FROM django_rest_passwordreset_resetpasswordtoken WHERE key = %s", (token,))
        reset_sent = cursor.fetchone()
        reset_sent_status = reset_sent[0]
        cursor.close()
    if ( reset_sent_status != True ):        
        # TODO: --EMAIL LOGIC GOES HERE-- Boilerplate to send new password reset email with token:
        # Update user to reset sent status
        with connection.cursor() as cursor:
            cursor.execute("UPDATE django_rest_passwordreset_resetpasswordtoken SET reset_sent = True WHERE key = %s", (token,))
            cursor.close()
        return HttpResponse('Reset email sent.')
    else:
        return HttpResponse('Reset email already sent.')
    
# Sample Action Logic + Response
## Receives a food via GraphQL > returns whether it's a hotdog
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_hotdog(request):    
    req_body = json.loads(request.body)
    food = req_body['input']['food']
    if food == 'hotdog':
        response = { 'hotdog':'true' }
    else:
        response = { 'hotdog':'false' }
    return HttpResponse(json.dumps(response))