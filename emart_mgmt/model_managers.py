from django.db import models
from django.utils.text import slugify


class CategoryManager(models.Manager):
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        for obj in objs:
            obj.name = obj.name.lower().strip()
            obj.slug = slugify(obj.name)

        super().bulk_create(objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts)


class ProductManager(models.Manager):
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        for obj in objs:
            obj.name = obj.name.lower().strip()
            obj.slug = slugify(obj.name)

        super().bulk_create(objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts)
