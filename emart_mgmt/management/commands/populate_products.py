import json
from django.conf import settings
from django.core.management import BaseCommand
from django.core.management.base import no_translations
from django.db import transaction

from core.type_class import UserType
from emart_mgmt import models as emart_mgmt_models
from accounts import models as accounts_models


class Command(BaseCommand):
    help = 'Trains intent'

    @no_translations
    @transaction.atomic
    def handle(self, *args, **options):
        path = settings.BASE_DIR / "emart_mgmt/management/commands/products.json"
        file = open(path, 'r')

        user = accounts_models.User.objects.filter(user_type=UserType.CUSTOMER).first()
        if not user:
            print('add user first')
            return

        product_list = json.load(file)
        category_dict = dict()
        product_obj_list = list()

        for product in product_list:
            category_name = str(product['productCategory']).strip().lower()
            if category_name not in category_dict:
                category_dict[category_name] = emart_mgmt_models.Category(
                    name=category_name
                )

            product_obj_list.append(
                emart_mgmt_models.Product(
                    id=product['productId'],
                    category=category_dict[category_name],
                    name=product['productName'],
                    image=product['productImage'],
                    in_stock=product['productStock'],
                    price=product['productPrice'],
                    sale_price=product['salePrice'],
                    seller=user

                )
            )

        category_obj_lists_to_bulk_create = list(category_dict.values())
        emart_mgmt_models.Category.objects.bulk_create(category_obj_lists_to_bulk_create,
                                                       ignore_conflicts=True)
        emart_mgmt_models.Product.objects.bulk_create(
            product_obj_list
        )
