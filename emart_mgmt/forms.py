from django import forms

from emart_mgmt.models import Product


class ProductForm(forms.ModelForm):
    category_id = forms.CharField(max_length=24, min_length=24)

    class Meta:
        model = Product
        fields = ['category_id', 'name', 'image', 'in_stock', 'price', 'sale_price']

    def clean_price(self):
        price = self.cleaned_data.get('price', 0)
        if not price:
            raise forms.ValidationError('Enter Price greater than 0')
        return price

    def clean_sale_price(self):
        sale_price = self.cleaned_data.get('sale_price', 0)
        if not sale_price:
            raise forms.ValidationError('Sale Price cannot be less than 1')

        return sale_price
