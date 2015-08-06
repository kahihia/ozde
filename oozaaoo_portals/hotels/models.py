from django.db import models

class citylist( models.Model ):
   cityid=models.CharField(max_length=50, null=False)   	   
   cityname= models.CharField(max_length=50, null=True, blank=True)
   countryname= models.CharField(max_length=50, null=True, blank=True)
   countrycode= models.CharField(max_length=50, null=True, blank=True)

   def __unicode__(self):
    return self.countrycode
