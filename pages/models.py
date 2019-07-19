from django.db import models

# Create your models here.
class QF(models.Model):
	Name_of_Generic_Medicine 	= models.CharField(max_length=80)
	Your_Email_id 				= models.CharField(max_length=80)
	Address						= models.CharField(max_length=80)
									

