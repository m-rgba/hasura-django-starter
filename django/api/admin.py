from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from api.models import Profile

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class profileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (profileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)