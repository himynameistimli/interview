from django.db import models


class UsernameType(models.TextChoices):
    EMAIL = 'E'
    MOBILE = 'M'


class UserType(models.TextChoices):
    ADMIN = 'A'
    STAFF = 'S'
    CUSTOMER = 'C'


class AuthProvider(models.TextChoices):
    DJANGO = 'D'
    GOOGLE = 'G'
    FACEBOOK = 'F'
    OTP = 'O'


class OperationType(models.TextChoices):
    CREATE = 'C'
    EDIT = 'E'
    DELETE = 'D'


class FriendStatusType(models.TextChoices):
    SENT = 'S'
    RECEIVED = "R"
    ACCEPTED = 'A'
