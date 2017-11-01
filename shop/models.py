from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .validators import *
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import pdb
# Create your models here.



from .storages import PicsStorage


class Product(models.Model):
	name=models.CharField(max_length=200)
	description=models.TextField(blank=True)
	create_timestamp=models.DateField(auto_now_add=True)
	update_timestamp=models.DateField(auto_now=True)
	def __str__(self):
		return str(self.name)



class Picture(models.Model):
	name=models.CharField(max_length=100,blank=True)
	picfile=models.ImageField(storage=PicsStorage(),blank=True)
	product = models.ForeignKey(
				'Product',
				on_delete=models.CASCADE,
				related_name='pics',
	)
	def __str__(self):
		return str(self.name)



@receiver(pre_delete, sender=Picture)
def my_handler(sender,instance,**kwargs):
	instance.picfile.delete()