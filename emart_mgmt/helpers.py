from django.db.models import F

from emart_mgmt import models as emart_mgmt_models


def get_product_details_by_product_id(current_user, product_id):
    product = emart_mgmt_models.Product.objects.filter(
        id=product_id,
        is_active=True,
    ).annotate(
        category_name=F('category__name')
    ).values(
        'id',
        'name',
        'category_id',
        'category_name',
        'image',
        'in_stock',
        'price',
        'sale_price',
        'slug',
        'seller',
        'created_on',
        'updated_on',
    )
    return product.first()
