from django.contrib.auth.models import BaseUserManager
from core.type_class import UserType
import logging
logger = logging.getLogger(__name__)


class UserModelManager(BaseUserManager):

    def _create_user(self, username, password, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have username')

        if is_superuser:
            user = self.model(
                username=username,
                user_type=UserType.ADMIN,
                is_staff=True,
                is_superuser=True,
                **extra_fields
            )
            logger.info("User got created, id: %s, is_superuser: %s" % (user.id, is_superuser))
        else:
            user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        print('create supseruser called')
        user = self._create_user(username, password, True, **extra_fields)
        return user
