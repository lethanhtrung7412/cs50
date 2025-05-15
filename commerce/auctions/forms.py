from django import forms
from .models import Category

class CategoryForm(forms.Form):
    category_name = forms.CharField(label="Name")

class ListingForm(forms.Form):
    product_name = forms.CharField(label="Product name", max_length=100)
    img = forms.URLField(label="Image link")
    bid_price = forms.DecimalField(label="Price")
    category = forms.MultipleChoiceField(
        choices=Category.objects.get(),
        label="Category"
    )