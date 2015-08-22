# Create your views here.
import requests
import logging
import random
import string
from django.utils import simplejson
from json import dumps, loads
import simplejson as json

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.context_processors import csrf 
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.contrib.auth.tokens import default_token_generator
from urllib import unquote, urlencode, unquote_plus
from django.conf import settings
from django.utils.http import urlquote
from urllib import urlencode
from urllib import unquote_plus
from django.utils import simplejson as json
from django.contrib.auth import authenticate, login
from payu.models import *

class goibiboAPI(object):

	''' Goibibo Py Client'''
	BASE = "http://pp.goibibobusiness.com/api/hotels/b2b/"
	BASE_BUS = "http://pp.goibibobusiness.com/api/bus/"

	def __init__(self, username, password):
		self.username = username
		self.password = password	

	def getHotelsByCity(self):
		import requests
		return (requests.get(self.BASE + "get_city_list", auth=(self.username, self.password)).json())

	def SearchHotelsByCity(self, cityid, checkin, checkout,rooms,adults1=0, nochildrens1=0,childage1_1=0,childage2_1=0, adults2=0, nochildrens2=0,childage1_2=0,childage2_2=0, adults3=0, nochildrens3=0,childage1_3=0,childage2_3=0, adults4=0, nochildrens4=0,childage1_4=0,childage2_4=0):
		if rooms=='4':
			query = self.BASE + "get_city_hotels" + "?query=hotels"+"-"+cityid+"-"+checkin+"-"+checkout+"-"+unicode(rooms)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3)+"-"+unicode(adults4)+"_"+unicode(nochildrens4)+"_"+unicode(childage1_4)+"_"+unicode(childage2_4) 
			
		elif rooms=='3':
			query = self.BASE + "get_city_hotels" + "?query=hotels"+"-"+cityid+"-"+checkin+"-"+checkout+"-"+unicode(rooms)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3) 
		elif rooms=='2':
			query = self.BASE + "get_city_hotels" + "?query=hotels"+"-"+cityid+"-"+checkin+"-"+checkout+"-"+unicode(rooms)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2) 
		else:
			query = self.BASE + "get_city_hotels" + "?query=hotels"+"-"+cityid+"-"+checkin+"-"+checkout+"-"+unicode(rooms)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1) 
		return query, (requests.get(query, auth=(self.username, self.password)).json())

	def getHotelDetailsByCity(self, joindata, hc, ibp, fwdp):
		print "hotelcode ======>", hc
		query = self.BASE + "get_hotel_details" + "?query=hotels"+"-"+joindata+"&hc="+hc+"&ibp=v3"+"&fwdp=''"
		print "search details ======>", query
		return query, (requests.get(query, auth=(self.username, self.password)).json())

	def getHotelReviewsDetails(self, hc):
		print "hotelcode ======>", hc
		query = self.BASE + "get_hotel_review" + "?hc="+hc
		print "HotelReviews ======>", query
		print "response", requests.get(query, auth=(self.username, self.password)).json()
		return (requests.get(query, auth=(self.username, self.password)).json())

	def getHotelCancelPolicy(self):
		return (requests.get(query, auth=(self.username, self.password)).json())

	def provisionalbooking(self, joindata, hc, ibp, fwdp, rtc, rpc):
		print "hotelcode ======>", hc
		query = self.BASE + "provisional_booking" + "?query=hotels"+"-"+joindata+"&hc="+hc+"&ibp="+ibp+"&rtc="+rtc+"&rpc="+rpc
		prbook = {'fwdp':{ }, 'customer_details':{"firstname" : "abc", "lastname" : "xyz", "email" : "xyz@abc.com", "mobile": "1234567891", "country_phone_code" : "+91", "title" : "Mr"}}
		print "provisionalbooking ======>", query           
		print "prbook ======>", prbook
		return (requests.post(query, data=prbook, auth=(self.username, self.password)).json())
		
	def BookingStatus(self, gobookingid):
		query = self.BASE + "get_booking_status?gobookingid="+gobookingid
		return (requests.get(query, auth=(self.username, self.password)).json())

	def BookingDetails(self, gobookingid):
		query = self.BASE + "get_booking_details?gobookingid="+gobookingid
		return (requests.get(query, auth=(self.username, self.password)).json())

	def RefundDetails(self, gobookingid):
		query = self.BASE + "get_refund_details?gobookingid="+gobookingid
		return (requests.get(query, auth=(self.username, self.password)).json())




		#=========================BUS API===============================#
	def Searchbus(self,source,destination,dateofdeparture,dateofarrival,trip):
		if trip == 'oneway':
			query = self.BASE_BUS+"search/?format=json&source="+source+"&destination="+destination+"&dateofdeparture="+str(dateofdeparture)
		else:
			query = self.BASE_BUS+"search/?format=json&source="+source+"&destination="+destination+"&dateofdeparture="+str(dateofdeparture)+"&dateofarrival="+str(dateofarrival)
		return query, (requests.get(query, auth=(self.username, self.password)).json())

	def Busseat(self,skey):
		query = self.BASE_BUS+"seatmap/?skey="+skey
		return query, (requests.get(query, auth=(self.username, self.password)).json())

	def CancelPolicy(self,skey):
		query=self.BASE_BUS+"cp/?skey="+skey
		return query,(requests.get(query, auth=(self.username, self.password)).json()) 

	def CancelTicket(self,pid):
		query=self.BASE_BUS+"cancel/?pid="+pid+"skey=asd"
		return query,(requests.get(query, auth=(self.username, self.password)).json())

	def BookConform(self,secret,bookingid,clientkey):
		query=self.BASE_BUS+"bookticket/?bookingid="+bookingid+"&secret="+secret+"&clientkey="+clientkey
		return query,(requests.get(query, auth=(self.username, self.password)).json())
		
	def BookStatus(self,pid):
		query=self.BASE_BUS+"status/?pid="+pid
		return query,(requests.get(query, auth=(self.username, self.password)).json())

			#=========================Flight API===============================#	

	# def FlightSearch(self, source, destination, dateofdeparture, dateofarrival=None, seatingclass="E", adults=1, children=0, infants=0):
	# 	if dateofarrival:
	# 		dateda = "&dateofdeparture=%d\
	# 		&dateofarrival%d" % (dateofdeparture, dateofarrival)
	# 	else:
	# 		dateda = "&dateofdeparture=%d" % dateofdeparture

	# 	# return (requests.get(self.BASE + ""search/" + "?format=json" + "&source=%s" % source + "&destination=%s" % destination + 
	# 	# 	dateda + "&seatingclass=%s" % seatingclass + "&adults=%d" % adults + "&children=%d" % children + "&infants=%d" % infants,
	# 	# 	params=self.auth).json())	

	# def GetHotelData(self, id_list):
	# 	id_list = str(id_list)\
	# 	.replace(" ", "")\
	# 	.replace("L", "")\
	# 	.replace(",", "%2C+")\
	# 	.replace("[", "%5B")\
	# 	.replace("]", "%5D")
	# 	return (requests.get(self.BASE + "voyager/" + "?method=hotels.get_hotels_data" + "&id_list=%s" % id_list + "&id_type=_id", params=self.auth).json())

	# def GetHotelPriceByCity(self, city_id, check_in, check_out):
	# 	return (requests.get(self.BASE + "cyclone/" + "?city_id=%d" % city_id + "&check_in=%d" % check_in + "&check_out=%d" % check_out, params=self.auth).json())

def format_redirect_url(redirect_path, query_string):
    ''' utility to format redirect url with fixido query string
    '''
    stop_popup = True if 'st=' in query_string else False
    
    url_join_str = '?'
    if url_join_str in redirect_path:
        redirect_path, qs = redirect_path.split(url_join_str, 1)
        query_string = qs + '&' + query_string
    
    qs = {}
    for q in query_string.split('&'):
        if '=' in q:
            k, v = q.split('=', 1)
            qs[k] = v
    
    if stop_popup:
        if qs.has_key('zr'): del qs['zr']
        if qs.has_key('lr'): del qs['lr']
        if qs.has_key('ler'): del qs['ler']
        if qs.has_key('thanks'): del qs['thanks']
    
    query_string = ''
    for k in qs:
        query_string += k + '=' + qs[k] + '&'
        
    return redirect_path + url_join_str + query_string[:-1]

def store_payudetails(request):
	#Code for storing Payu Details
	payudetails=PayuDetails()
	payudetails.mihpayid=request.POST.get('mihpayid')
	payudetails.userprofile=UserProfile.objects.get(user=request.user)
	payudetails.mode=request.POST.get('mode')
	payudetails.status=request.POST.get('status')
	payudetails.unmappedstatus=request.POST.get('unmappedstatus')
	payudetails.key=request.POST.get('key')
	payudetails.txnid=request.POST.get('txnid')
	payudetails.amount=request.POST.get('amount')
	payudetails.cardCategory=request.POST.get('cardCategory')
	payudetails.discount=request.POST.get('discount')
	payudetails.net_amount_debit=request.POST.get('net_amount_debit')
	payudetails.addedon=request.POST.get('addedon')
	payudetails.productinfo=request.POST.get('productinfo')
	payudetails.hash=request.POST.get('hash')
	payudetails.payment_source=request.POST.get('payment_source')
	payudetails.PG_TYPE=request.POST.get('PG_TYPE')
	payudetails.bank_ref_num=request.POST.get('bank_ref_num')
	payudetails.bankcode=request.POST.get('bankcode')
	payudetails.error=request.POST.get('error')
	payudetails.error_Message=request.POST.get('error_Message')
	payudetails.name_on_card=request.POST.get('name_on_card')
	payudetails.cardnum=request.POST.get('cardnum')
	payudetails.issuing_bank=request.POST.get('issuing_bank')
	payudetails.card_type=request.POST.get('card_type')
	payudetails.save()

	# response.set_cookie('payudetails',payudetails.id)
	# response.set_cookie('payustatus',payudetails.status)
	return payudetails.id,payudetails.status

def fileopen(request):
	f = open("example.txt", "w")

def fileclose(request):
	f.close()

