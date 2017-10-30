from django.core.exceptions import ValidationError 
from django.conf import settings
import os

def validate_ajaxpreload(instance):
	fi=os.path.join(settings.MEDIA_ROOT+'pics/', instance.name)
	if os.path.exists(fi):		
		raise ValidationError('Файл с таким именем уже загружен')
  