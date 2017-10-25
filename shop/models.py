from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.


class Product(models.Model):
	name=models.CharField(max_length=200, null=True)
	description=models.TextField()
	create_timestamp=models.DateField(auto_now_add=True)
	update_timestamp=models.DateField(auto_now=True)
	def __str__(self):
		return str(self.name)



class Picture(models.Model):
	name=models.CharField(max_length=100, null=True)
	picfile=models.FileField(upload_to='pics',storage=FileSystemStorage())
	product = models.ForeignKey(
				'Product',
				on_delete=models.CASCADE,
				related_name='product',
				null=True,
	)
	def __str__(self):
		return str(self.name)
