from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime
import os

class AjaxTmpPreloadStorage(FileSystemStorage):
	def get_available_name(self, name, max_length=100):
		if self.exists(name):
			os.remove(os.path.join(settings.MEDIA_ROOT, name))
		return name

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