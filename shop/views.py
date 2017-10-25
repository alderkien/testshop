from django.shortcuts import render
from django.views.generic import ListView

from .models import *



def index(request):
	return render(request, 'testshop/site.html',)

class Products(ListView):
	model = Product
	paginate_by = 10

