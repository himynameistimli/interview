from django.db.models import F, Q
from django.forms import model_to_dict
from django.utils import timezone
from rest_framework import status

from core import core_lib
from core.type_class import OperationType, FriendStatusType
from emart_mgmt import models as emart_mgmt_models
from emart_mgmt import helpers as emart_mgmt_helpers
from emart_mgmt import forms as emart_mgmt_forms
from accounts import models as accounts_models

def get_product_list(request, current_user, data, is_app=False, http_response=True,
                     raise_exception=True):
    res = core_lib.init_response_dict()
    try:
        # if there are some more things like filters, sortings then create another helper function
        # which will be called from here

        start, limit, page, count = core_lib.pagination_helper(data, default_count=10)

        product_list = emart_mgmt_models.Product.objects.filter(
            is_active=True
        ).annotate(
            category_name=F('category__name'),
        ).values(
            'id',
            'name',
            'category_name',
            'image',
            'in_stock',
            'price',
            'sale_price',
            'slug',
            'seller_id',
            'created_on',
        ).order_by('-updated_on', 'id')[start:limit]

        res['status'] = True
        res['cv']['product_list'] = list(product_list)
        res['cv']['next'] = None if len(product_list) < count else page + 1
        res['cv']['prev'] = page - 1 if page > 1 else 1
        res['cv']['page'] = page

        return res
    except Exception as ex:
        return core_lib.handle_exception(exception_object=ex,
                                         print_exception=True,
                                         raise_exception=raise_exception,
                                         http_response=http_response)


def get_product_detail(request, current_user, product_id, data, is_app=False,
                       http_response=True, raise_exception=True):
    res = core_lib.init_response_dict()
    try:
        product = emart_mgmt_helpers.get_product_details_by_product_id(current_user, product_id)
        if not product:
            res['status'] = False
            res['errors']['__all__'].append('Product Does Not Exist')
            res['response_status'] = status.HTTP_404_NOT_FOUND
            return res

        # save user View data
        viewed_product, created = emart_mgmt_models.UserProductView.objects.get_or_create(
            user_id=current_user.id,
            product_id=product_id
        )
        if not created:
            viewed_product.view_count = viewed_product.view_count + 1
        else:
            viewed_product.view_count = 1

        viewed_product.save()

        res['cv']['product'] = product
        res['status'] = True
        return res
    except Exception as ex:
        return core_lib.handle_exception(exception_object=ex,
                                         print_exception=True,
                                         raise_exception=raise_exception,
                                         http_response=http_response)


def get_product_form_data(request, current_user, data, operation, product_id=None,
                          is_app=False, http_response=True, raise_exception=True):
    res = core_lib.init_response_dict()
    try:
        if operation not in [OperationType.CREATE, OperationType.EDIT]:
            raise Exception('Invalid Operation')

        if operation == OperationType.EDIT and product_id:
            product = emart_mgmt_helpers.get_product_details_by_product_id(current_user, product_id)
            if not product:
                res['status'] = False
                res['response_status'] = status.HTTP_404_NOT_FOUND
                res['errors']['__all__'].append('Product does not exist')
                return res
            else:
                res['cv']['product'] = product

        category_list = emart_mgmt_models.Category.objects.filter(is_active=True).values(
            'id', 'name'
        )
        res['cv']['category_list'] = list(category_list)
        res['status'] = True
        return res
    except Exception as ex:
        return core_lib.handle_exception(exception_object=ex,
                                         print_exception=True,
                                         raise_exception=raise_exception,
                                         http_response=http_response)


def add_edit_delete_product(request, current_user, data, operation, product_id=None,
                            is_app=False, http_response=True, raise_exception=False):
    res = core_lib.init_response_dict()
    try:
        if operation in [OperationType.EDIT, OperationType.DELETE] and not product_id:
            raise Exception('Product id is required')

        form_instance = None
        if operation in [OperationType.EDIT, OperationType.DELETE]:
            product = emart_mgmt_models.Product.get_product_by_id(product_id)
            if not product:
                res['status'] = False
                res['errors']['__all__'].append('Product Does Not Exist')
                res['response_status'] = status.HTTP_404_NOT_FOUND
                return res
            else:
                form_instance = product
            if product.seller_id != current_user.id:
                res['status'] = False
                res['errors']['__all__'].append('Unauthorized Access')
                res['response_status'] = status.HTTP_401_UNAUTHORIZED
                return res

            if operation == OperationType.DELETE:
                product.delete()
                res['status'] = True
                res['cv']['success'] = True
                res['cv']['message'] = 'Product Deleted Successfully'
                return res

        form = emart_mgmt_forms.ProductForm(data=data, instance=form_instance)
        if form.is_valid():
            current_date_time = timezone.now()
            product = form.save(commit=False)
            product.category_id = form.cleaned_data['category_id']
            product.seller = current_user

            if operation == OperationType.CREATE:
                last_product = emart_mgmt_models.Product.objects.last()
                product.id = last_product.id + 1

            product.updated_on = current_date_time
            product.save()
            res['status'] = True
            return res
        else:
            res['errors'] = form.errors
            return res

    except Exception as ex:
        return core_lib.handle_exception(exception_object=ex,
                                         print_exception=True,
                                         raise_exception=raise_exception,
                                         http_response=http_response)


def get_recommended_product_by_user(request, current_user, data, is_app=False, http_response=True,
                                    raise_exception=True):
    res = core_lib.init_response_dict()
    try:
        user_friend_id_list = list(accounts_models.UserFriends.objects.filter(
            user_id=current_user.id,
            status=FriendStatusType.ACCEPTED
        ).values_list('friend_id', flat=True))

        recommended_product_id_list = emart_mgmt_models.UserProductView.objects.filter(
            user_id__in=user_friend_id_list
        ).order_by('-view_count').values_list('product_id', flat=True)[:10]

        recommended_product_list = emart_mgmt_models.Product.objects.filter(
            is_active=True,
            id__in = recommended_product_id_list
        ).annotate(
            category_name=F('category__name'),
        ).values(
            'id',
            'name',
            'category_name',
            'image',
            'in_stock',
            'price',
            'sale_price',
            'slug',
            'seller_id',
            'created_on',
        ).order_by('?')

        res['status'] = True
        res['cv']['recommended_product_list'] = list(recommended_product_list)
        return res

    except Exception as ex:
        return core_lib.handle_exception(exception_object=ex,
                                         print_exception=True,
                                         raise_exception=raise_exception,
                                         http_response=http_response)
