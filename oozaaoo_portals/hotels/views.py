import requests
import logging
import random
import string
import json
from django.utils import simplejson
from json import dumps, loads
import simplejson as json


from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from templated_email import send_templated_mail
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from hotels.forms import RegistrationForm

from hotels.models import *
from apiservice.views import *

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.context_processors import csrf 
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from urllib import unquote, urlencode, unquote_plus
from django.conf import settings
from django.utils.http import urlquote
from urllib import urlencode
from urllib import unquote_plus
from django.utils import simplejson as json
from django.http import HttpResponse
from django.utils import simplejson


def registration(request):
	"""
	User Registration
	"""
	message = None
	registration_form = RegistrationForm()
	if 'user_registration' in request.POST:
		registration_form = RegistrationForm(request.POST)
		if registration_form.is_valid():		
			user = User.objects.create_user(
				username=registration_form.cleaned_data["email"],
				first_name=registration_form.cleaned_data["first_name"],
				email=registration_form.cleaned_data["email"],
				)
			user.set_password(registration_form.cleaned_data["password"])
			user.save()			

			send_templated_mail(
				template_name='welcome',
				from_email='testmail123sample@gmail.com',
				recipient_list=[registration_form.cleaned_data["email"]],
				context={
					'username': registration_form.cleaned_data["email"],
					'name': registration_form.cleaned_data["first_name"],
				},
			)
			message = "You have successfully completed registration."
	return render_to_response('login-register.html', {'message': message, 'registration_form':registration_form},
							  context_instance=RequestContext(request))
							  
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
    return render_to_response('login.html', context_instance=RequestContext(request))

def home(request):
	"""
	Home Page for Travel Portal
	"""
	from hotels.models import citylist	
	return render_to_response("hotels/home.html", context_instance=RequestContext(request))


def getcitylist(request):
	"""
	Ajax Load in Auto Complete in Home Page City List
	"""
	from collections import OrderedDict
	results = []
	unsort_dict = {}
	key_loc = request.GET.get('term')
	city_lists = citylist.objects.filter(cityname__icontains=key_loc)

	for city_list in city_lists:
		cityname = city_list.cityname.strip()
		cityid = city_list.cityid
		countryname = city_list.countryname
		unsort_dict[cityname] = {'cityid':cityid, 'label':cityname, 'value':cityname}

	sorted_dic = OrderedDict(sorted(unsort_dict.iteritems(), key=lambda v: v[0]))
	for k, v in sorted_dic.iteritems():  
		results.append(v)

	return HttpResponse(simplejson.dumps(results), mimetype='application/json')
	# return render_to_response("hotels/home.html", context_instance=RequestContext(request))

def loadcitylist(request):
	from collections import OrderedDict
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')		
	getcityresponse = GO.getHotelsByCity()

	results = []
	unsort_dict = {}
	key_loc = request.GET.get('term')
	for key, value in getcityresponse['data'].iteritems():
		keycode =  key
		countryname =  value.get('country_name')
		cityname = value.get('city_name').encode('ascii', 'ignore')
		countrycode = value.get('country_code')
		unsort_dict[citylist] = {'keycode':keycode, 'coutryname':countryname, 'cityname':cityname, 'countrycode':countrycode}
		obj = citylist()
		obj.cityid = 	keycode
		obj.cityname = 	cityname
		obj.countryname = countryname
		obj.countrycode = countrycode
		obj.save()
		print "====>>>>", unsort_dict[citylist]

	sorted_dict = OrderedDict(sorted(unsort_dict.iteritems(), key=lambda v:v[0])) 	
	for k, v in sorted_dict.iteritems():
		results.append(v)

	print 'results', results
	return HttpResponse(simplejson.dumps(results), mimetype='application/json')
	

# /** To get the Search Results based on CityId, ChecIn, Checkout, Adults, Roooms, Children **/
def gethotellist(request):	
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	# if request.COOKIES.get('filterkeyword')=='':
	# 	print 'true'
	# else:
	#  	print 'false'
	cityid=request.POST.get('filterkeyword',request.COOKIES.get('filterkeyword'))
	# cityid = request.COOKIES.get('filterkeyword')
	# #cityid=request.COOKIES.get('filterkeyword')
	# print 'cityid',cityid
	checkin = request.POST.get('start',request.COOKIES.get('checkin'))
	checkinvalue = checkin.replace('/','')
	checkout = request.POST.get('end',request.COOKIES.get('checkout'))
	checkoutvalue = checkout.replace('/','')
	rooms1 = request.POST.get('room1', '1')
	adults1 = request.POST.get('adults1', '1')	
	nochildrens1 = request.POST.get('childs1', '0')
	childage1_1 = request.POST.get('childage1_1', '0')
	childage2_1 = request.POST.get('childage2_1', '0')
	rooms2 = request.POST.get('room2', '0')
	adults2 = request.POST.get('adults2', '0')	
	nochildrens2 = request.POST.get('childs2', '0')
	childage1_2 = request.POST.get('childage1_2', '0')
	childage2_2 = request.POST.get('childage2_2', '0')
	rooms3 = request.POST.get('room3', '0')
	adults3 = request.POST.get('adults3', '0')	
	nochildrens3 = request.POST.get('childs3', '0')
	childage1_3= request.POST.get('childage1_3', '0')
	childage2_3 = request.POST.get('childage2_3', '0')
	rooms4 = request.POST.get('room4', '0')
	adults4 = request.POST.get('adults4', '0')	
	nochildrens4 = request.POST.get('childs4', '0')
	childage1_4 = request.POST.get('childage1_4', '0')
	childage2_4 = request.POST.get('childage2_4', '0')

	if rooms4=='4':
		rooms=4
		getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms4, adults1, nochildrens1,childage1_1,childage2_1, adults2, nochildrens2,childage1_2,childage2_2, adults3, nochildrens3,childage1_3,childage2_3, adults4, nochildrens1,childage1_4,childage2_4,)	
	elif rooms3=='3':
		rooms=3
		getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms3,adults1, nochildrens1,childage1_1,childage2_1, adults2, nochildrens2,childage1_2,childage2_2, adults3, nochildrens3,childage1_3,childage2_3)
	elif rooms2=='2':
		rooms=2
		getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms2,adults1, nochildrens1,childage1_1,childage2_1, adults2, nochildrens2,childage1_2,childage2_2)
	else:
		print '=================1'
		rooms=1
		getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms1,adults1, nochildrens1,childage1_1,childage2_1)


	cityFields = ['country']
	city = {}
	for k, v in getcityresponse['data']['city_meta_info'].iteritems():
		if k in cityFields:
			city[k] = v

	hotelFields = ['prc', 'hn', 'hr', 'hc', 'fwdp', 'c', 't', 'ibp']
	hotels = []
	for hotel in getcityresponse['data']['city_hotel_info']:
		_hotel = {}
		# _hotel = {'hn':hotel['hn']}
		for k, v in hotel.iteritems():
			if k in hotelFields:
				_hotel[k] = v
		hotels.append(_hotel)

	# response  = {'city':city, 'hotels':hotels}
	# return HttpResponse(simplejson.dumps(hotels), mimetype='application/json')
	if rooms4=='4':
		joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms3)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3)+"-"+unicode(adults4)+"_"+unicode(nochildrens4)+"_"+unicode(childage1_4)+"_"+unicode(childage2_4)
	elif rooms3=='3':
		joindata= unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms3)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3)
	elif rooms2=='2':
		joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms2)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)
	else:
		joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms1)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)	
	response = render_to_response("hotels/hotels.html", {'city':city, 'hotels':hotels, 'joindata':joindata}, context_instance=RequestContext(request))
  	
  	response.set_cookie( 'joindata', joindata )
  	response.set_cookie( 'checkin', checkin )
  	response.set_cookie( 'checkout', checkout )
  	response.set_cookie('filterkeyword',unicode(cityid))

	return response

def gethoteldetails(request):		
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')			
	joindata = request.COOKIES.get('joindata')
	hc = request.POST.get('hc',request.COOKIES.get('hc'))	
	ibp = request.POST.get('ibp',request.COOKIES.get('ibp'))
	fwdp =request.POST.get('fwdp',request.COOKIES.get('fwdp'))

	gethoteldetailresponse = GO.getHotelDetailsByCity(joindata, hc, ibp, fwdp)
	gethotelreviewresponse = GO.getHotelReviewsDetails(hc)

	# # /** Hotel  Details */
	hoteldetails = ['prc', 'pincode', 'room_count', 'vcid', 'hn', 'address', 'c', 'des']
	_hotel = {}
	for k, v in gethoteldetailresponse['data'].iteritems():		
		# _hotel = {'hn':hotel['hn']}		
		if k in hoteldetails:
			_hotel[k] = v

	# /** Hotel  Gallery Image */		
	_hotel['gallery']= gethoteldetailresponse['data']['gallery']

	hotelroominfos = []
	for hotelroominfo in gethoteldetailresponse['data']['rooms_data']:		
		_rhotelinfo = {'rtc':hotelroominfo['rtc'], 'rpc':hotelroominfo['rpc']}
		hotelroominfos.append(_rhotelinfo)	

	# /** Hotel  Reviews Details */		
	hotelreviewsFields = ['hotelName', 'firstName', 'lastName', 'hotelCity', 'totalRating', 'reviewContent', 'createdAt', 'reviewTitle']	
	reviews = []
	for hotelreview in gethotelreviewresponse['data']:
		review = {}
		for f in hotelreviewsFields:
			if f in hotelreview:
			 		review[f] = hotelreview[f]
			else:
					review[f] = None
		reviews.append(review)

	morehoteldata = {'joindata':joindata, 'hc':hc, 'ibp':ibp, 'fwdp':fwdp}	

	# reviews = []
	# for hotelreview in gethotelreviewresponse['data']:
	# 	_rhotel = {'hotelName':hotelreview['hotelName'], 'totalRating':hotelreview['totalRating'], 'hotelCity':hotelreview['hotelCity'], 'reviewContent':hotelreview['reviewContent'], 'firstName':hotelreview['firstName']}
	# 	reviews.append(_rhotel)

	#return HttpResponse(simplejson.dumps(gethoteldetailresponse), mimetype='application/json')
	response = render_to_response("hotels/hoteldetails.html", {'hotels':_hotel , 'reviews':reviews, 'morehoteldatas':morehoteldata, 'hotelroominfos':hotelroominfos }, context_instance=RequestContext(request))
	response.set_cookie('hc',hc)
	response.set_cookie('ibp',ibp)
	response.set_cookie('fwdp',fwdp)
	return response

def setprovisionalbooking(request):
	from django.utils import simplejson
	 # GO = goibiboAPI('apitesting@goibibo.com', 'test123')			
	# joindata = request.POST['joindata']
	# hc = request.POST['hc']	
	# ibp = request.POST['ibp']
	# fwdp = request.POST['fwdp']
	# rtc = request.POST['rtc']
	# rpc = request.POST['rpc']	
	# gethoteldetailresponse = GO.provisionalbooking(joindata, hc, ibp, fwdp, rtc, rpc)	
	import urllib
	import requests
	url = "http://pp.goibibobusiness.com/api/hotels/b2b/provisional_booking/"
	querystring = {"query":"hotels-7247861711286471145-20150807-20150811-1-1_0_0","hc":"3769018583127607778","ibp":"v3","rtc":"45000011170","rpc":"990000014478"}
	payload = {'fwdp':'{}', 'customer_details':'{ "firstname":"sastha","lastname":"Mano", "email":"sastha@ymail.com", "mobile":"9876543201","country_phone_code":"+91", "title":"Mr"}'}
	# payload = "fwdp=%7B%7D&customer_details=%7B%20%22firstname%22%20%3A%22sastha%22%2C%20%22lastname%22%20%3A%20%22Mano%22%2C%20%22email%22%20%3A%20%22sastha%40ymail.com%22%2C%20%22mobile%22%20%3A%20%229876543201%22%2C%20%22country_phone_code%22%20%3A%20%22%2B91%22%2C%20%22title%22%3A%20%22Mr%22%20%7D"
	headers = {
	'content-type': "application/x-www-form-urlencoded"
	}
	response = requests.request("POST", url, data=payload,headers=headers, params=querystring, auth=('apitesting@goibibo.com','test123'))
	print "res", response.json()	
	return HttpResponse(response)
	#return render_to_response("hotels/hotel-payment.html", context_instance=RequestContext(request))	

def confirmbooking(request):
	from django.utils import simplejson
	import urllib
	import requests
	from hashlib import md5, sha512
	createhash = 'test123' + 'GOHTLDV2ee67a1438838485' + '|'+ str(22748) + '|' + 'hotels-7247861711286471145-20150807-20150811-1-1_0_0'.lower()+ '|' + 'sastha'.lower() + '|' + 'sastha@ymail.com' + '|' + 'temp'  + '|'  + 'true' + '|' +"travelibibo"
	createhash = sha512(createhash).hexdigest()
	url = "http://pp.goibibobusiness.com/api/hotels/b2b/confirm_booking/"
	payload = {'secretkey':'e626d3fd2b76978ee0f9760e9c6de47a56f928c6edc0910f65eafcb398dc512156298210d6caaa1cd5767745a5547e34fc8bf0890b7300a494c19ec230e8e1f3', 'gobookingid':'GOHTLDV2ee67a1438838485'}
	headers = {
	'content-type': "application/x-www-form-urlencoded"
	}
	response = requests.request("POST", url, data=payload,headers=headers, auth=('apitesting@goibibo.com','test123'))
	return HttpResponse(response)

def getbookingstatus(request):
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	gobookingid='GOHTLDV2ee67a1438838485'
	bookingstatus=GO.BookingStatus(gobookingid)
	return HttpResponse(simplejson.dumps(bookingstatus['data']), mimetype='application/json')

def getbookingdetails(request):
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	gobookingid='GOHTLDV2ee67a1438838485'
	bookingstatus=GO.BookingDetails(gobookingid)
	status={}
	status['RoomType']=bookingstatus['data']['RoomType']
	status['ci']=bookingstatus['data']['ci']
	status['bookingid']=bookingstatus['data']['bookingid']
	status['HotelName']=bookingstatus['data']['HotelName']
	status['firstname']=bookingstatus['data']['customer_details']['firstname']
	status['title']=bookingstatus['data']['customer_details']['title']
	status['mobile']=bookingstatus['data']['customer_details']['mobile']
	status['lastname']=bookingstatus['data']['customer_details']['lastname']
	status['country_phone_code']=bookingstatus['data']['customer_details']['country_phone_code']
	status['email']=bookingstatus['data']['customer_details']['email']
	status['HotelAddress']=bookingstatus['data']['HotelAddress']
	status['gobookingid']=bookingstatus['data']['gobookingid']
	status['phone']=bookingstatus['data']['phone']
	status['noofNights']=bookingstatus['data']['noofNights']
	status['noofChildren']=bookingstatus['data']['noofChildren']
	status['cancelPolicy']=bookingstatus['data']['cpdata']['cancelPolicy']
	status['hotelPolicy']=bookingstatus['data']['cpdata']['hotelPolicy']
	status['hc']=bookingstatus['data']['hc']
	status['noofAdults']=bookingstatus['data']['noofAdults']

	return HttpResponse(simplejson.dumps(status), mimetype='application/json')

def getrefund(request):
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	gobookingid='GOHTLDV2ee67a1438838485'
	getrefund=GO.RefundDetails(gobookingid)
	return HttpResponse(simplejson.dumps(getrefund['data']['refund_details']), mimetype='application/json')

def confirmcancel(request):
	from django.utils import simplejson
	import urllib
	import requests
	url = "http://pp.goibibobusiness.com/api/hotels/b2b/confirm_cancel"
	payload = {'gobookingid':'GOHTLDV2ee67a1438838485'}
	headers = {
	'content-type': "application/x-www-form-urlencoded"
	}
	response = requests.request("POST", url, data=payload,headers=headers, auth=('apitesting@goibibo.com','test123'))
	return HttpResponse(response)