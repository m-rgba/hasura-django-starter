from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4

def generateUUID():
    return str(uuid4())

class Role(models.Model):
    name = models.CharField(max_length=120, unique=True)
    uuid = models.UUIDField(default=generateUUID, unique=True)
    
def get_user_role():
    return Role.objects.get_or_create(name="user")[0]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=get_user_role)
    registration_sent = models.BooleanField(default=False)
    uuid = models.UUIDField(default=generateUUID, unique=True)
    
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()