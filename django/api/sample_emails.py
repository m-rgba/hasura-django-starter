from rest_framework import serializers, status, permissions, generics, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User 
from api.models import Profile
from django.db import connection
from django.http import HttpResponse
from email.message import EmailMessage
from collections import namedtuple
import requests
import logging
import json
import smtplib  
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        # ------- BOILERPLATE NEW USER EMAIL : Uncomment this section for emails -------
        # # Email Creds
        # email_smtp_from = 'YourFrom:Email'  
        # email_smtp_from_name = 'YourName'
        # email_smtp_auth_user = 'AuthUsername'
        # email_smtp_auth_pass = 'AuthPassword'
        # email_smtp_auth_host = 'AuthHost'
        # email_smtp_auth_port = 587
        # # Compose
        # emai_subject = 'Your new account has been created'
        # email_plaintext = ('Welcome! Your new account has been created.')
        # email_html = '<strong>Welcome to our service!</strong> Your new account has been created.'
        # msg = MIMEMultipart('alternative')
        # msg['Subject'] = emai_subject
        # msg['From'] = '"'+ email_smtp_from_name +'"' + ' <' + email_smtp_from + '>'
        # msg['To'] = email
        # part1 = MIMEText(email_plaintext, 'plain')
        # part2 = MIMEText(email_html, 'html')
        # msg.attach(part1)
        # msg.attach(part2)
        # # Send
        # server = smtplib.SMTP(email_smtp_auth_host, email_smtp_auth_port)
        # server.ehlo()
        # server.starttls()
        # server.ehlo()
        # server.login(email_smtp_auth_user, email_smtp_auth_pass)
        # server.sendmail(email_smtp_from, email, msg.as_string())
        # server.close()

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
        # ------- BOILERPLATE PASSWORD RESET EMAIL : Uncomment this section for emails -------
        # What happens? 1 Embed token in URL link > 2 pass token as querystring to client > 3 client calls back to REST API w/ token, email, new password ( /api/reset_password/confirm/ )
        # # Email Creds
        # email_smtp_from = 'YourFrom:Email'  
        # email_smtp_from_name = 'YourName'
        # email_smtp_auth_user = 'AuthUsername'
        # email_smtp_auth_pass = 'AuthPassword'
        # email_smtp_auth_host = 'AuthHost'
        # email_smtp_auth_port = 587
        # # Compose
        # emai_subject = 'A password reset has been requested for your account.'
        # email_plaintext = ('A password reset has been requested for your account. Please click the following link to reset your password. Reset your password at https://www.google.com/search?q=' + token )
        # email_html = '<strong>A password reset has been requested for your account.</strong><br /> Please click the following link to reset your password:<br /> <a href="https://www.google.com/search?q=' + token + '">Testing password reset link</a>'
        # msg = MIMEMultipart('alternative')
        # msg['Subject'] = emai_subject
        # msg['From'] = '"'+ email_smtp_from_name +'"' + ' <' + email_smtp_from + '>'
        # msg['To'] = email
        # part1 = MIMEText(email_plaintext, 'plain')
        # part2 = MIMEText(email_html, 'html')
        # msg.attach(part1)
        # msg.attach(part2)
        # # Send
        # server = smtplib.SMTP(email_smtp_auth_host, email_smtp_auth_port)
        # server.ehlo()
        # server.starttls()
        # server.ehlo()
        # server.login(email_smtp_auth_user, email_smtp_auth_pass)
        # server.sendmail(email_smtp_from, email, msg.as_string())
        # server.close()

        # Update user to reset sent status
        with connection.cursor() as cursor:
            cursor.execute("UPDATE django_rest_passwordreset_resetpasswordtoken SET reset_sent = True WHERE key = %s", (token,))
            cursor.close()
        return HttpResponse('Reset email sent.')
    
    else:
        return HttpResponse('Reset email already sent.')