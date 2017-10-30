from django.shortcuts import render
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime

import os



import json


from .forms import ProductWithPicFormSet
from .models import *

class TmpStorage(FileSystemStorage):
	location=settings.MEDIA_ROOT+'/tmp'
	base_url=settings.MEDIA_URL+'tmp/'
	minutes_before_del=30
	def save(self,*args,**kwargs):
		self.drop_old_files()
		return super().save(*args,**kwargs)
	def get_available_name(self, name, max_length=100):
		if self.exists(name):
			os.remove(os.path.join(self.location, name))
		return name

	def drop_old_files(self):
		ldir=self.listdir('')
		now=datetime.now()
		for f in ldir[1]:
			d=now-self.created_time(f)
			if d.seconds>self.minutes_before_del*60:
				self.delete(f)

class AjaxableResponseMixin(object):
	def render_to_json_response(self, context, **response_kwargs):
		data = json.dumps(context)
		response_kwargs['content_type'] = 'application/json'
		return HttpResponse(data, **response_kwargs)


def index(request):
	return render(request, 'testshop/site.html',)




class Products(ListView):
	model = Product
	paginate_by=5

	def get_queryset(self):
		return Product.objects.prefetch_related('pics').all()

class ProductCreate(CreateView,AjaxableResponseMixin):

	model = Product
	fields = ['name','description']
	success_url='/list/'

	def post(self, request, *args, **kwargs): 
		#request.upload_handlers.insert(0, TemporaryFileUploadHandler(request))
		if (self.request.is_ajax()):
			files = request.FILES
			myfile = request.FILES['img']
			fs = TmpStorage()
			filename = fs.save(myfile.name, myfile)
			uploaded_file_url = fs.url(filename)
			context_dict = {
				'result': 'ok',
				'tmpfile': uploaded_file_url,
			}
			return self.render_to_json_response(context_dict)
		else:
			return super(CreateView,self).post(self, request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		data = super(ProductCreate, self).get_context_data(**kwargs)
		if self.request.POST:
			print(self.request.FILES)
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


class ProductUpdate(UpdateView):

	model = Product
	fields = ['name','description']
	success_url='/list/'

	def post(self, request, *args, **kwargs): 
		if (self.request.is_ajax()):
			context_dict = {
				'result': 'ok',
				'tmpfile': '/media/pics/1415640644854_3N08JPQ.jpg.50x50_q85_crop.jpg',
			}
			return self.render_to_json_response(context_dict)
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
