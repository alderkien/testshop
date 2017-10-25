from django.conf.urls import url

from . import views

from .views import *

urlpatterns = [
	url(r'products_list/', Products.as_view()),
	url(r'$', views.index, name='index'),

]