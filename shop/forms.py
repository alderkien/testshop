from django import forms
from django.forms.models import inlineformset_factory
from .models import Product,Picture


class ProductForm(forms.ModelForm):
	model = Product
	fields = ['name','description']

class PictureForm(forms.ModelForm):
	model = Picture


ProductWithPicFormSet = inlineformset_factory(Product, Picture,
                                            form=PictureForm,exclude=[], extra=1)

