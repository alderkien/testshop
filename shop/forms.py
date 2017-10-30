from django import forms
from django.forms.models import inlineformset_factory
from django.core.files import File
from django.forms import ImageField
from .models import Product,Picture
from .validators import *
from .storages import TmpStorage
from django.core.files.images import ImageFile
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
			fl=ts.path(picfile_str)
			shutil.move(fl,os.path.join(settings.MEDIA_ROOT+'pics/',picfile_str))
			self.cleaned_data['picfile']='pics/'+picfile_str

		return self.cleaned_data

	def save(self, commit=True):
		return super(PictureForm, self).save(commit=commit)
		
	class Meta:
		model = Picture
		fields = ['name', 'picfile', 'product','picfile_str']

ProductWithPicFormSet = inlineformset_factory(Product, Picture,form=PictureForm,fields=['name', 'picfile', 'product','picfile_str'])

