from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from core import core_lib
from emart_mgmt import emart_mgmt_lib


def product_list_renderer(request):
    try:
        template_name = 'emart_mgmt/product_list.html'
        res = emart_mgmt_lib.get_product_list(request,
                                              current_user=request.user,
                                              data=request.GET,
                                              is_app=False,
                                              http_response=True,
                                              raise_exception=True)
        if 'status' in res and res['status'] is True:
            return render(request, template_name, {'cv': res['cv']})
        else:
            return core_lib.return_multi_key_json_response(['errors'],
                                                           res['errors'] if 'errors' in res else None
                                                           )
    except Exception as ex:
        return core_lib.handle_exception(print_exception=True, http_response=True,
                                         raise_exception=True)


def product_detail_renderer(request, product_id):
    try:
        template_name = 'emart_mgmt/product_detail.html'
        res = emart_mgmt_lib.get_product_detail(request,
                                                current_user=request.user,
                                                product_id=product_id,
                                                data=request.GET,
                                                is_app=False,
                                                http_response=True,
                                                raise_exception=False)
        if 'status' in res and res['status'] is True:
            return render(request, template_name, {'cv': res['cv']})
        else:
            return core_lib.return_multi_key_json_response(['errors'],
                                                           res['errors'] if 'errors' in res else None
                                                           )
    except Exception as ex:
        return core_lib.handle_exception(print_exception=True, http_response=True,
                                         raise_exception=True)


def add_edit_product_renderer(request, operation, product_id=None):
    try:
        res = emart_mgmt_lib.get_product_form_data(
            request,
            current_user=request.user,
            data=request.GET,
            operation=operation,
            product_id=product_id,
            is_app=False,
            http_response=True,
            raise_exception=True,
        )
        if 'status' in res and res['status'] is True:
            return render(request, 'emart_mgmt/product_form.html', {'cv': res['cv']})
        else:
            return core_lib.return_multi_key_json_response(
                ['errors'], [res['errors'] if 'errors' in res else None]
            )
    except Exception as ex:
        return core_lib.handle_exception(print_exception=True, http_response=True,
                                         raise_exception=True)


def add_edit_delete_product_handler(request, operation, product_id):
    try:
        res = emart_mgmt_lib.add_edit_delete_product(
            request,
            current_user=request.user,
            data=request.POST,
            operation=operation,
            product_id=product_id,
            is_app=False,
            http_response=True,
            raise_exception=True,
        )
        if 'status' in res and res['status'] is True:
            success_url = reverse('emart_mgmt:product_list')
            return core_lib.return_multi_key_json_response(['success', 'success_url'], [True, success_url])
        else:
            return core_lib.return_multi_key_json_response(
                ['errors'], [res['errors'] if 'errors' in res else 'Something Went Wrong']
            )
    except Exception as ex:
        return core_lib.handle_exception(print_exception=True, http_response=True,
                                         raise_exception=True)


def recommended_product_renderer(request):
    try:
        res = emart_mgmt_lib.get_recommended_product_by_user(
            request,
            current_user=request.user,
            data=request.GET,
            is_app=False,
            http_response=True,

        )
        if 'status' in res and res['status'] is True:
            if request.is_ajax():
                content = render_to_string(request=request, template_name='emart_mgmt/recommended_product_list.html',
                                           context={'cv': res['cv']})
                return core_lib.return_multi_key_json_response(['success', 'content'],
                                                               [True, content])

            return render(request, 'emart_mgmt/recommended_product_list.html', {'cv': res['cv']})
        else:
            return core_lib.return_multi_key_json_response(
                ['errors'], [res['errors'] if 'errors' in res else 'Something Went Wrong']
            )

    except Exception as ex:
        return core_lib.handle_exception(print_exception=True, http_response=True,
                                         raise_exception=True)
