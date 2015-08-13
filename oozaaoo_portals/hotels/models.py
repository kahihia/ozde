from django.db import models
from django.contrib.auth.models import User
import datetime

class citylist( models.Model ):
   cityid=models.CharField(max_length=50, null=False)   	   
   cityname= models.CharField(max_length=50, null=True, blank=True)
   countryname= models.CharField(max_length=50, null=True, blank=True)
   countrycode= models.CharField(max_length=50, null=True, blank=True)

   def __unicode__(self):
    return self.countrycode

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    name=models.CharField(max_length=50, null=True, blank=True)
    phone=models.CharField(max_length=50, null=True, blank=True)
    dateofbirth=models.DateTimeField()
    def __unicode__(self):
        return self.user.username      