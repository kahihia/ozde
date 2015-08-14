from django.db import models
from uuid import uuid4
from uuid import UUID
import uuid
from django_extensions.db.fields import UUIDField
from hotels.models import *


# class MyOrder(models.Model):

#     items = models.CharField(max_length=500, null=True, blank=True)
#     order_date = models.DateField(auto_now=True)
#     buyer = models.CharField(max_length=500, null=True, blank=True)

#     txnid = models.CharField(max_length=36, primary_key=True)
#     amount = models.FloatField(null=True, blank=True,default=0.0)
#     hash = models.CharField(max_length=500, null=True, blank=True)
#     billing_name = models.CharField(max_length=500, null=True, blank=True)
#     billing_street_address = models.CharField(max_length=500, null=True, blank=True)
#     billing_country = models.CharField(max_length=500, null=True, blank=True)
#     billing_state = models.CharField(max_length=500, null=True, blank=True)
#     billing_city = models.CharField(max_length=500, null=True, blank=True)
#     billing_pincode = models.CharField(max_length=500, null=True, blank=True)
#     billing_mobile = models.CharField(max_length=500, null=True, blank=True)
#     billing_email = models.CharField(max_length=500, null=True, blank=True)

#     shipping_name = models.CharField(max_length=500, null=True, blank=True)
#     shipping_street_address = models.CharField(max_length=500, null=True, blank=True)
#     shipping_country = models.CharField(max_length=500, null=True, blank=True)
#     shipping_state = models.CharField(max_length=500, null=True, blank=True)
#     shipping_city = models.CharField(max_length=500, null=True, blank=True)
#     shipping_pincode = models.CharField(max_length=500, null=True, blank=True)
#     shipping_mobile = models.CharField(max_length=500, null=True, blank=True)
#     shipping_rate = models.FloatField(null=False, blank=False, default=0.0)
#     status = models.CharField(max_length=500, null=True, blank=True)
#     shipping_email = models.CharField(max_length=500, null=True, blank=True)

#     payment_method = models.CharField(max_length=1000,verbose_name='Payment-method')
#     is_paid = models.BooleanField(default=False)
#     is_delivered = models.BooleanField(default=False)
#     is_accepted = models.BooleanField(default=False)

class PayuDetails(models.Model):
    mihpayid = models.CharField(max_length=100, null=True, blank=True)
    userprofile=models.ForeignKey(UserProfile)
    mode = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    unmappedstatus =models.CharField(max_length=20, null=True, blank=True)
    key =models.CharField(max_length=50, null=True, blank=True)
    txnid=models.CharField(max_length=50, null=True, blank=True)
    amount =models.FloatField(default=0.0,null=True, blank=True)
    cardCategory=models.CharField(max_length=20, null=True, blank=True)
    discount =models.FloatField(default=0.0,null=True, blank=True)
    net_amount_debit=models.FloatField(default=0.0,null=True, blank=True)
    addedon=models.DateTimeField(default=datetime.datetime.now)
    productinfo=models.CharField(max_length=50, null=True, blank=True)
    hash=models.CharField(max_length=250, null=True, blank=True)
    payment_source =models.CharField(max_length=20, null=True, blank=True)
    PG_TYPE=models.CharField(max_length=20, null=True, blank=True)
    bank_ref_num=models.CharField(max_length=50, null=True, blank=True)
    bankcode= models.CharField(max_length=20, null=True, blank=True)
    error=models.CharField(max_length=20, null=True, blank=True)
    error_Message =models.CharField(max_length=100, null=True, blank=True)
    name_on_card =models.CharField(max_length=50, null=True, blank=True)
    cardnum=models.CharField(max_length=20, null=True, blank=True)
    issuing_bank=models.CharField(max_length=50, null=True, blank=True)
    card_type =models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return self.mihpayid







