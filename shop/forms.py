from django import forms
from django.forms.models import inlineformset_factory
from .models import Product,Picture


class ProductForm(forms.ModelForm):
	model = Product
	fields = ['name','description']

class PictureForm(forms.ModelForm):
	model = Picture
	fields = ['name','picfile']


ProductWithPicFormSet = inlineformset_factory(Product, Picture,
                                            form=PictureForm, fields=['name','picfile'], extra=1)

