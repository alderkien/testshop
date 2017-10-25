from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView


from .models import *




def index(request):
	return render(request, 'testshop/site.html',)

class Products(ListView):
	model = Product
	paginate_by = 10

class ProductCreate(CreateView):
	model = Product
	fields = ['name','description']

