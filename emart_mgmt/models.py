from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from core import core_lib

# Create your models here.
from emart_mgmt.model_managers import CategoryManager, ProductManager
from accounts import models as accounts_model


class Category(models.Model):
    id = models.CharField(max_length=24, primary_key=True, db_index=True, default=core_lib.generate_unique_object_id)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, blank=True)
    objects = CategoryManager()

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.name = self.name.lower().strip()
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    # assuming one product can belongs to only category
    objects = ProductManager()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.URLField()
    in_stock = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=17, decimal_places=12)
    sale_price = models.DecimalField(max_digits=17, decimal_places=12)
    slug = models.SlugField(max_length=300, blank=True)
    seller = models.ForeignKey(accounts_model.User, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @staticmethod
    def get_product_by_id(product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist as ex:
            return None


class UserProductView(models.Model):
    id = models.CharField(max_length=24, primary_key=True, default=core_lib.generate_unique_object_id, db_index=True)

    user = models.ForeignKey(accounts_model.User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=1)

    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
