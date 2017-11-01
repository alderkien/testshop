from django.shortcuts import render
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView
from django.http import HttpResponse

from django.conf import settings

from django.core.files.base import File
from django.core.files.uploadedfile import UploadedFile
import pdb

import json
from .forms import ProductWithPicFormSet
from .storages import TmpStorage
from .models import *



def index(request):
	return render(request, 'testshop/site.html',)


class ImgPreloadMixin(object):
	def render_to_json_response(self, context, **response_kwargs):
		data = json.dumps(context)
		response_kwargs['content_type'] = 'application/json'
		return HttpResponse(data, **response_kwargs)

	def ajaxImgLoad(self, request, *args, **kwargs):
		myfile = request.FILES['img']
		fs = TmpStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		context_dict = {
			'result': 'ok',
			'path':fs.url(''),
			'tmpfile': filename,
		}
		return self.render_to_json_response(context_dict)
		

class Products(ListView):
	model = Product
	paginate_by=10

	def get_queryset(self):
		return Product.objects.prefetch_related('pics').all()

class ProductCreate(CreateView,ImgPreloadMixin):

	model = Product
	fields = ['name','description']
	success_url='/list/'

	def post(self, request, *args, **kwargs): 
		if (self.request.is_ajax()):
			return self.ajaxImgLoad(request, *args, **kwargs)
		else:
			return super(CreateView,self).post(self, request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		data = super(ProductCreate, self).get_context_data(**kwargs)
		if self.request.POST:
			data['pics'] = ProductWithPicFormSet(self.request.POST,self.request.FILES)
		else:
			data['pics'] = ProductWithPicFormSet()
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		formset = context['pics']
		
		if formset.is_valid():
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			return redirect(self.success_url)
		else:
			return self.render_to_response(self.get_context_data(form=form))


class ProductUpdate(UpdateView,ImgPreloadMixin):

	model = Product
	fields = ['name','description']
	success_url='/list/'

	def post(self, request, *args, **kwargs): 
		if (self.request.is_ajax()):
			return self.ajaxImgLoad(request, *args, **kwargs)
		else:
			return super(UpdateView,self).post(self, request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		data = super(ProductUpdate, self).get_context_data(**kwargs)
		if self.request.POST:
			data['pics'] = ProductWithPicFormSet(self.request.POST,self.request.FILES,instance=self.object)
			data['pics'].full_clean()
		else:
			data['pics'] = ProductWithPicFormSet(instance=self.object)
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		formset = context['pics']
		if formset.is_valid():
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			return redirect(self.success_url)
		else:
			return self.render_to_response(self.get_context_data(form=form))
