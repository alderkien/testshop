from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'list/$', Products.as_view()),
	url(r'create/$', ProductCreate.as_view(), name='products_create'),
]