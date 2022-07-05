from django import forms
from .models import *

class CreateListForm(forms.Form):
	item_name = forms.CharField(label="", required=True, widget = forms.TextInput(attrs={'class': 'form-control','placeholder': 'Item Name'}))
	floor_price = forms.IntegerField(label="", required=True, widget = forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Floor Price'}))
	item_image = forms.URLField(label="", required=False, widget = forms.URLInput(attrs={'class': 'form-control','placeholder': 'Item Image URL'}))
	description = forms.CharField(label="", required=False, widget = forms.Textarea(attrs={'class': 'form-control','placeholder': 'Description'}))
	item_category = forms.CharField(label="", required=False, widget = forms.TextInput(attrs={'class': 'form-control','placeholder': 'Item Category'}))