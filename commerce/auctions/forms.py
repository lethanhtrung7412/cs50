from django import forms
from .models import Category, Listing, Bidding

class CategoryForm(forms.Form):
    category_name = forms.CharField(label="Name")

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['product_name', 'img', 'bid_price', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label_from_instance = lambda obj: obj.name
