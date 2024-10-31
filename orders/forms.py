from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    address = forms.CharField()
    
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
