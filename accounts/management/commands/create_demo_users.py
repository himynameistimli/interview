import json
from django.conf import settings
from django.core.management import BaseCommand
from django.core.management.base import no_translations
from django.db import transaction

from core.type_class import UserType, UsernameType, AuthProvider, FriendStatusType
from emart_mgmt import models as emart_mgmt_models
from accounts import models as accounts_models


class Command(BaseCommand):
    help = 'Create user Demo data '

    @no_translations
    @transaction.atomic
    def handle(self, *args, **options):
        path = settings.BASE_DIR / "emart_mgmt/management/commands/products.json"
        file = open(path, 'r')

        for i in range(1, 4):
            email = 'user{}@gmail.com'.format(i)
            user = accounts_models.User(username=email,
                                        username_type=UsernameType.EMAIL,
                                        first_name='user{}'.format(i),
                                        last_name='name',
                                        email=email,
                                        is_email_verified=True,
                                        user_type=UserType.CUSTOMER,
                                        auth_provider=AuthProvider.DJANGO,
                                        )
            password = 'Password@123'
            user.set_password(password)
            self.stdout.write('{} created'.format(email))
            user.save()

        self.stdout.write('Creating friends')

        users = accounts_models.User.objects.filter(
            user_type = UserType.CUSTOMER
        )

        user_friend_obj_list = list()
        for user in users:
            for friend in users:
                if user.id != friend.id:
                    user_friend_obj_list.append(
                        accounts_models.UserFriends(
                            user=user,
                            friend=friend,
                            status=FriendStatusType.ACCEPTED
                        )
                    )

        accounts_models.UserFriends.objects.bulk_create(user_friend_obj_list)
        self.stdout.write('User Created Successfully')

        user = accounts_models.User(username='user4@gmail.com',
                                    username_type=UsernameType.EMAIL,
                                    first_name='user4',
                                    last_name='name',
                                    email='user4@gmail.com',
                                    is_email_verified=True,
                                    user_type=UserType.CUSTOMER,
                                    auth_provider=AuthProvider.DJANGO,
                                    )

        user.set_password('Password@123')
        user.save()
