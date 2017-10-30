from django import forms
from django.forms.models import inlineformset_factory
from .models import Product,Picture

"""
class ProductForm(forms.ModelForm):
	model = Product
	fields = ['name','description']
"""
class PictureForm(forms.ModelForm):
	model = Picture
	def __init__(self, *args, **kwargs):
		super(PictureForm, self).__init__(*args, **kwargs)
		self.fields['picfile'].widget.attrs['class'] = 'fileAjaxUpload'
		self.fields['picfile'].widget.attrs['style'] = 'width: 130px;'


#ProductWithPicFormSet = inlineformset_factory(Product, Picture,form=PictureForm,exclude=[], extra=1)
ProductWithPicFormSet = inlineformset_factory(Product, Picture,form=PictureForm,exclude=[])

