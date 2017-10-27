from django.shortcuts import render
from django.db import transaction
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .forms import ProductForm, ProductWithPicFormSet
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
			data['pics'] = ProductWithPicFormSet(self.request.POST)
		else:
			data['pics'] = ProductWithPicFormSet()
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		pics = context['pics']
		with transaction.atomic():
			self.object = form.save()
		if pics.is_valid():
			pics.product = self.object
			pics.save()

		return super(ProductCreate, self).form_valid(form)
