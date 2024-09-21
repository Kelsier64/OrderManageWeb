from django import forms
from base.models import Product
class OrderForm(forms.Form):
    input_notes = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'order'}))
    quantity = forms.IntegerField(initial=0, min_value=0,required=False,widget=forms.NumberInput(attrs={'class': 'order'}))
    