from django.contrib import admin
from django.contrib.admin import register

from emart_mgmt import models as emart_mgmt_models


# Register your models here.


@register(emart_mgmt_models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@register(emart_mgmt_models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@register(emart_mgmt_models.UserProductView)
class UserProductViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'view_count']
