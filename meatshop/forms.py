from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["meat_code", "meat_name", "meat_in_price", "meat_sell_price"]
        widgets = {
            "meat_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Kod (unique)"}),
            "meat_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nomi"}),
            "meat_in_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "meat_sell_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
        }
