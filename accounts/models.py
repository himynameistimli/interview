from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Q
from django.utils import timezone

from accounts.model_managers import UserModelManager
from core import core_lib

# Create your models here.
from core.type_class import UsernameType, UserType, AuthProvider, FriendStatusType


class User(AbstractBaseUser, PermissionsMixin):
    """
     user can register with mobile, email , social login,

    """
    # id = models.CharField(max_length=24, primary_key=True, default=core_lib.generate_unique_object_id, db_index=True)

    username = models.CharField(max_length=150, unique=True, blank=False, null=False, db_index=True)
    username_type = models.CharField(max_length=1, choices=UsernameType.choices, default=UsernameType.EMAIL)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    profile_photo = models.ImageField(blank=True, null=True, upload_to='uploads')
    dob = models.DateField(blank=True, null=True)
    # gender = models.CharField(choices=GenderType.choices, max_length=1, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    mobile = models.CharField(max_length=10, blank=True, null=True)
    is_mobile_verified = models.BooleanField(default=False)
    mobile_verification_otp = models.CharField(max_length=6, blank=True, null=True)

    user_type = models.CharField(max_length=1, choices=UserType.choices,
                                 default=UserType.CUSTOMER)

    auth_provider = models.CharField(max_length=1, choices=AuthProvider.choices,
                                     default=AuthProvider.DJANGO)

    is_created_anonymously = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    objects = UserModelManager()

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class UserFriends(models.Model):
    id = models.CharField(max_length=24, primary_key=True, default=core_lib.generate_unique_object_id, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    status = models.CharField(max_length=1, choices=FriendStatusType.choices, default=FriendStatusType.SENT)

    created_on = models.DateTimeField(default=timezone.now, db_index=True)
    updated_on = models.DateTimeField(default=timezone.now)

    @staticmethod
    def get_user_friend_qs_by_user_id(user_id):
        return UserFriends.objects.filter(
            user_id=user_id,
            status=FriendStatusType.ACCEPTED
        )
