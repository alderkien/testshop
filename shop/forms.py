from django import forms
from django.forms.models import inlineformset_factory
from .models import Product,Picture
from .validators import *
from .storages import TmpStorage,PicsStorage
import shutil
import pdb

class PictureForm(forms.ModelForm):
	picfile_str=forms.CharField(widget = forms.HiddenInput(), required = False)
	def __init__(self, *args, **kwargs):
		super(PictureForm, self).__init__(*args, **kwargs)
		self.fields['picfile'].widget.attrs['class'] = 'fileAjaxUpload'
		self.fields['picfile'].widget.attrs['style'] = 'width: 130px;'

	def clean(self):
		picfile_str = self.cleaned_data.get('picfile_str')
		picfile = self.cleaned_data.get('picfile')
		if not picfile_str and not picfile:
			raise forms.ValidationError('Хоть как-то картинка должна передаться')
		elif picfile_str:
			ts=TmpStorage()
			ps=PicsStorage()
			#pdb.set_trace()
			picfile=ps.save(picfile_str,ts.open(picfile_str))
			ts.delete(picfile_str)
			self.cleaned_data['picfile']=picfile

		return self.cleaned_data

	def save(self, commit=True):
		return super(PictureForm, self).save(commit=commit)
		
	class Meta:
		model = Picture
		fields = ['name', 'picfile', 'product','picfile_str']

ProductWithPicFormSet = inlineformset_factory(Product, Picture,form=PictureForm,fields=['name', 'picfile', 'product','picfile_str'],extra=1)

