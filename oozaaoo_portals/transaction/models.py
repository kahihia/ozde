from django.db import models
from hotels.models import *
# Create your models here.
from payu.models import *

class Order(models.Model):
    userprofile=models.ForeignKey(UserProfile)
    #Hotel fields
    hotelcode=models.CharField(max_length=50, null=True, blank=True)
    hotelname=models.CharField(max_length=50, null=True, blank=True)
    hotelcity=models.CharField(max_length=50, null=True, blank=True)
    checkin=models.DateField(null=True,blank=True)
    checkout=models.DateField(null=True,blank=True)
    rooms=models.IntegerField(null=True,blank=True)
    guest=models.IntegerField(null=True,blank=True)  
    #Bus Fields
    trip=models.CharField(max_length=50, null=True, blank=True)
    source=models.CharField(max_length=50, null=True, blank=True)
    destination=models.CharField(max_length=50, null=True, blank=True)
    start_date=models.DateField(null=True,blank=True)
    end_date=models.DateField(null=True,blank=True)
    totalseats=models.IntegerField(null=True,blank=True)
    boardingpoint_id=models.CharField(max_length=50,null=True,blank=True)
    boardingpoint_name=models.CharField(max_length=200,null=True,blank=True)
    #Common
    amount=models.FloatField(default=0.0,null=True,blank=True)
    category_type=models.CharField(max_length=20,null=True,blank=True)
    created_date=models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.id

class OrderList(models.Model):
    order=models.ForeignKey(Order)
    #Hotels
    room=models.IntegerField(null=True, blank=True)
    adults=models.IntegerField(null=True, blank=True)
    children=models.IntegerField(null=True, blank=True)
    child1_age=models.IntegerField(null=True, blank=True)
    child2_age=models.IntegerField(null=True, blank=True)
    #Bus
    seatnumber=models.CharField(max_length=10, null=True, blank=True)
    firstname=models.CharField(max_length=50, null=True, blank=True)
    lastname=models.CharField(max_length=50, null=True, blank=True)
    age=models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.id

class Transaction(models.Model):
    order=models.ForeignKey(Order)
    payu_details=models.ForeignKey(PayuDetails)
    #Hotels
    provisionalbooking_id=models.CharField(max_length=50, null=True, blank=True)
    confirmationbooking_id=models.CharField(max_length=50, null=True, blank=True)
    productinfo=models.CharField(max_length=100, null=True, blank=True)
    provisionalbooking_status=models.CharField(max_length=20, null=True, blank=True)
    confirmationbooking_status=models.CharField(max_length=20, null=True, blank=True)
    #Bus
    tentativebooking_id=models.CharField(max_length=50, null=True, blank=True)
    tentativebooking_status=models.CharField(max_length=20, null=True, blank=True)
    #Common
    payu_status=models.CharField(max_length=20, null=True, blank=True)
    created_date=models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.id
