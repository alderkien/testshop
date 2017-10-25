from django import forms
from .models import Product,Picture


class ProductForm(forms.ModelForm):
	model = Product
	fields = ['name','description']

class PictureForm(forms.ModelForm):
	model = Picture
	fields = ['name','picfile']