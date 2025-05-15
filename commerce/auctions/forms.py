from django import forms

class ListingForm(forms.Form):
    product_name = forms.CharField(label="Product name", max_length=100)
    img = forms.URLField(label="Image link")
    bid_price = forms.DecimalField(label="Price")