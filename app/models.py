from django.db import models


class Language(models.Model):
	iso_639_3 = models.CharField(
		max_length = 3,
		unique = True,
		verbose_name = 'ISO 639-3'
	)
	iso_639_1 = models.CharField(
		max_length = 2,
		unique = True,
		null = True,
		blank = True,
		verbose_name = 'ISO 639-1'
	)
	
	latitude = models.FloatField(null=True)
	longitude = models.FloatField(null=True)
	
	class Meta:
		ordering = ['iso_639_3']
	
	def __str__(self):
		"""
		Returns the model's string representation.
		"""
		return self.iso_639_3


