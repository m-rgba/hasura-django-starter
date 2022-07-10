import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Role

class Command(BaseCommand):
    def handle(self, *args, **options):
        ## Create Initial User Role
        if not Role.objects.filter(name='user').exists():
            user_role = Role.objects.create(
                name='user',
            )
        else:
            print('User role already exists, skipping...')

        ## Create Other Roles
        if os.environ['DJANGO_ROLES']:
            try:
                roles_env = os.environ['DJANGO_ROLES']
                roles_list = [x.strip() for x in roles_env.split(',')]
                for role in roles_list:
                    if not Role.objects.filter(name=role).exists():
                        added_role = Role.objects.create(
                            name=role,
                        )
                    else:
                        print('Role already exists, skipping...')
            except Exception as e:
                print(e)
                print('Problem adding Role...')

        ## Create Initial Users
        if os.environ['DJANGO_DEFAULT_USERNAME'] and os.environ['DJANGO_DEFAULT_PASSWORD'] and os.environ['DJANGO_DEFAULT_ROLE']:
            try:
                if not User.objects.filter(email=os.environ['DJANGO_DEFAULT_EMAIL']).exists():
                    username = os.environ['DJANGO_DEFAULT_USERNAME']
                    email = os.environ['DJANGO_DEFAULT_EMAIL']
                    password = os.environ['DJANGO_DEFAULT_PASSWORD']
                    admin = User.objects.create_superuser(username, email, password)
                    admin.is_active = True
                    admin.is_admin = True
                    admin.save()
                else:
                    print('User already exists, skipping...')
            except Exception as e:
                print(e)
                print('Problem adding user...')