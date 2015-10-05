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
	
	@property
	def iso_code(self):
		"""
		Equals to ISO 639-1 if available and ISO 639-3 otherwise.
		That is how languages are referred to in .tsv files.
		"""
		if self.iso_639_1:
			return self.iso_639_1
		else:
			return self.iso_639_3
	
	def __str__(self):
		"""
		Returns the model's string representation.
		"""
		return self.iso_639_3
	
	def to_dict(self):
		"""
		Returns the model instance as a dictionary.
		"""
		return {
			'iso_639_3': self.iso_639_3,
			'iso_639_1': self.iso_639_1,
			'iso_code': self.iso_code,
			'latitude': self.latitude,
			'longitude': self.longitude
		}


