from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render
from django.views import generic
from django.views.generic.base import View

from core.type_class import OperationType
from emart_mgmt import models as emart_mgmt_models
from emart_mgmt import handlers as emart_mgmt_handlers


# Create your views here.
class ProductListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return emart_mgmt_handlers.product_list_renderer(
            request
        )


class ProductDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return emart_mgmt_handlers.product_detail_renderer(
            request,
            product_id=kwargs['product_id']
        )


class AddProductView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return emart_mgmt_handlers.add_edit_product_renderer(request,
                                                             operation=OperationType.CREATE,
                                                             product_id=None,
                                                             )

    def post(self, request, *args, **kwargs):
        return emart_mgmt_handlers.add_edit_delete_product_handler(request,
                                                                   operation=OperationType.CREATE,
                                                                   product_id=None,
                                                                   )


class EditProductView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return emart_mgmt_handlers.add_edit_product_renderer(request,
                                                             product_id=kwargs['product_id'],
                                                             operation=OperationType.EDIT)

    def post(self, request, *args, **kwargs):
        return emart_mgmt_handlers.add_edit_delete_product_handler(request,
                                                                   operation=OperationType.EDIT,
                                                                   product_id=kwargs['product_id'],
                                                                   )


class DeleteProductView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return emart_mgmt_handlers.add_edit_delete_product_handler(request,
                                                                   operation=OperationType.DELETE,
                                                                   product_id=kwargs['product_id'],
                                                                   )


class RecommendedProductView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return emart_mgmt_handlers.recommended_product_renderer(request,
                                                                )
