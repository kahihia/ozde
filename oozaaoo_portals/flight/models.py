from django.db import models

class IataManager(models.Manager):
    def get_query_set(self):
        return (super(IataManager, self).get_query_set().order_by('code'))

class Iata(models.Model):
	"""Storing Airport city,code,world area code,country,latitude,longitude"""
	city = models.CharField(max_length=150,help_text="City Name")
	code = models.CharField(max_length=50,help_text="Airport Code")
	worldareacode = models.CharField(max_length=50,help_text="World Code")
	country = models.CharField(max_length=150,help_text="Country Name")
	longitude = models.DecimalField(max_digits=9, decimal_places=6,help_text="Airport Longitude")
	latitude = models.DecimalField(max_digits=9, decimal_places=6,help_text="Airport Latitude")
	airportname = models.CharField(max_length=150,help_text="Airport Name")
	gmt = models.IntegerField(help_text="GMT")

	objects =  IataManager()

	def __unicode__(self):
		return self.country
