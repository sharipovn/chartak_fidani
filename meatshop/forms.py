from django import forms
from .models import Product,IncomeSale

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


class IncomeSaleForm(forms.ModelForm):
    class Meta:
        model = IncomeSale
        fields = ["meat", "quantity", "quantity_unit", "action_type", "operation_date", "from_where", "to_where"]
        widgets = {
            "meat": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "step": "0.001", "min": "0.001", "placeholder": "Miqdor"}),
            "quantity_unit": forms.Select(attrs={"class": "form-control"}),
            "action_type": forms.Select(attrs={"class": "form-control"}),
            "operation_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "from_where": forms.TextInput(attrs={"class": "form-control", "placeholder": "Qayerdan (Kirim)"}),
            "to_where": forms.TextInput(attrs={"class": "form-control", "placeholder": "Qayerga (Chiqim)"}),
        }
