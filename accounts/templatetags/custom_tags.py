import datetime
from datetime import timedelta

from django import template
from django.db.models import F
from django.template.defaultfilters import stringfilter
import json
from dateutil.parser import parse
from django.utils import timezone

from django.utils.safestring import mark_safe
from django.utils.html import urlize as urlize_impl

from core.type_class import FriendStatusType

register = template.Library()
from accounts import models as accounts_models


@register.filter
def get_friend_list(user):
    friend_email_list = list(accounts_models.UserFriends.objects.filter(
        user_id=user.id,
        status=FriendStatusType.ACCEPTED
    ).annotate(friend_email=F('friend__email')).values_list('friend_email', flat=True))

    html = ""
    for _email in friend_email_list:
        html = html + "<span> {} </span>".format(_email)

    return html
