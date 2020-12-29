from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4

def generateUUID():
    return str(uuid4())

ROLES=(
    ("user", "user"),
    ("editor", "editor")
)

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=120, choices=ROLES, default="user")
    registration_sent = models.BooleanField(default=False)
    uuid = models.UUIDField(default=generateUUID, unique=True)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()