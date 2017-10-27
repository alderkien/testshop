from django.shortcuts import render
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView

from .forms import ProductWithPicFormSet
from .models import *




def index(request):
	return render(request, 'testshop/site.html',)

class Products(ListView):
	model = Product
	paginate_by=5

	def get_queryset(self):
		return Product.objects.prefetch_related('pics').all()

class ProductCreate(CreateView):

	model = Product
	fields = ['name','description']
	success_url='/list/'

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


class ProductUpdate(UpdateView):

	model = Product
	fields = ['name','description']
	success_url='/list/'

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
