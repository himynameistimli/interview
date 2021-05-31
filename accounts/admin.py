from django.contrib import admin

# Register your models here.
from django.contrib.admin import register
from accounts import models as accounts_models


@register(accounts_models.User)
class UserAdmin(admin.ModelAdmin):
    pass


@register(accounts_models.UserFriends)
class UserFriendsAdmin(admin.ModelAdmin):
    pass
