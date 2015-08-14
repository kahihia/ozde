import requests
import logging
import random
import string
import json
from django.utils import simplejson
from json import dumps, loads
import simplejson as json
from django.views.decorators.csrf import csrf_exempt

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
from transaction.models import *

class mydict(dict):
        def __str__(self):
            return json.dumps(self)


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
	"""
	Login User
	"""
	logout(request)
	username = password = ''
	print request.POST['next']
	if request.POST["next"] is not "":
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	        if user.is_active:
	            login(request, user)
	            return HttpResponseRedirect(request.POST["next"])
	else:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
	return render_to_response('login-register.html', context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def myprofile(request):
	user = request.user
	userprofile=UserProfile.objects.get(pk=user.id)
	return render_to_response('myprofile.html',{'user':user,'userprofile':userprofile}, context_instance=RequestContext(request))


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
	"""
	To load the City Name and Id in Database 
	"""
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

	return HttpResponse(simplejson.dumps(results), mimetype='application/json')
	

# /** To get the Search Results based on CityId, ChecIn, Checkout, Adults, Roooms, Children **/
def gethotellist(request):
	"""
	Get the hotel list based on checkin and checkout values.
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')

	cityid=request.POST.get('filterkeyword',request.COOKIES.get('filterkeyword'))
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
		rooms=1
		getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms1,adults1, nochildrens1,childage1_1,childage2_1)


	cityFields = ['country']
	city = {}
	for k, v in getcityresponse['data']['city_meta_info'].iteritems():
		if k in cityFields:
			city[k] = v

	hotelFields = ['prc', 'hn', 'hr', 'hc', 'fwdp', 'c', 't', 'ibp','l','fm','offer_tag','gr']
	hotel_city=hotelFields[5]
	print hotel_city
	hotels = []
	for hotel in getcityresponse['data']['city_hotel_info']:
		_hotel = {}
		# _hotel = {'hn':hotel['hn']}
		for k, v in hotel.iteritems():
			if k in hotelFields:
				_hotel[k] = v
		hotels.append(_hotel)
		
		# if 'fm' in hotels:
		# 	hotel_fm=hotels.fm
		
  	if rooms4=='4':
		joindata = uncde(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms3)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3)+"-"+unicode(adults4)+"_"+unicode(nochildrens4)+"_"+unicode(childage1_4)+"_"+unicode(childage2_4)
		guest=int(adults1)+int(nochildrens1)+int(adults2)+int(nochildrens2)+int(adults3)+int(nochildrens3)+int(adults4)+int(nochildrens4)
	elif rooms3=='3':
		joindata= unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms3)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3)
		guest=int(adults1)+int(nochildrens1)+int(adults2)+int(nochildrens2)+int(adults3)+int(nochildrens3)
	elif rooms2=='2':
		joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms2)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)
		guest=int(adults1)+int(nochildrens1)+int(adults2)+int(nochildrens2)
	else:
		joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms1)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)	
		guest=int(adults1)+int(nochildrens1)
	
	response = render_to_response("hotels/hotels.html", {'city':city, 'hotels':hotels, 'joindata':joindata}, context_instance=RequestContext(request))
	response.set_cookie( 'joindata', joindata )
  	response.set_cookie( 'checkin', checkin )
  	response.set_cookie( 'checkout', checkout )
  	response.set_cookie('filterkeyword',unicode(cityid))
  	response.set_cookie('rooms',rooms)
  	response.set_cookie('guest',unicode(guest))
	return response

def gethoteldetails(request):
	"""
	Get the hotel Details based on list IBP(v3, v6) and FWDP.
	"""		
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')			
	joindata = request.COOKIES.get('joindata')
	hc = request.POST.get('hc',request.COOKIES.get('hc'))	
	ibp = request.POST.get('ibp',request.COOKIES.get('ibp'))
	fwdp =request.POST.get('fwdp',request.COOKIES.get('fwdp'))

	gethoteldetailresponse = GO.getHotelDetailsByCity(joindata, hc, ibp, fwdp)
	gethotelreviewresponse = GO.getHotelReviewsDetails(hc)

	# # /** Hotel  Details */
	hoteldetails = ['prc', 'pincode', 'room_count', 'vcid', 'hn', 'address', 'c', 'des','l','hr','gr','la','lo']
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
	hotelreviewsFields = ['hotelName', 'firstName', 'lastName', 'hotelCity', 'totalRating', 'reviewContent', 'createdAt', 'reviewTitle','attractions']	
	reviews = []
	for hotelreview in gethotelreviewresponse['data']:
		review = {}
		for f in hotelreviewsFields:
			if f in hotelreview:
			 		review[f] = hotelreview[f]
			else:
					review[f] = None
		reviews.append(review)
	print reviews

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
	response.set_cookie('rtc',hotelroominfo['rtc'])
	response.set_cookie('rpc',hotelroominfo['rpc'])
	response.set_cookie('hn',_hotel['hn'])
	response.set_cookie('prc',_hotel['prc'])
	response.set_cookie('c',_hotel['c'])
	response.set_cookie('l',_hotel['l'])
	response.set_cookie('hr',_hotel['hr'])
	return response
	
@login_required(login_url='/register/')
def userdetails(request):
	"""
	UserDetails for PayU Methods with Amount.
	"""	
	rtc = request.POST.get('rtc',request.COOKIES.get('rtc'))
	rpc = request.POST.get('rpc',request.COOKIES.get('rpc'))
	response= render_to_response("hotels/hotel-booking.html", context_instance=RequestContext(request))
	response.set_cookie('rtc',rtc)
	response.set_cookie('rpc',rpc)
	return response

@csrf_exempt
def setprovisionalbooking(request):
	from django.utils import simplejson
	import urllib
	import requests
	url = "http://pp.goibibobusiness.com/api/hotels/b2b/provisional_booking/"
	joindata={}
	joindata['query']= "hotels-"+request.COOKIES.get('joindata')
	joindata['hc']=request.COOKIES.get('hc')
	joindata['ibp']=request.COOKIES.get('ibp')
	joindata['rtc']=request.COOKIES.get('rtc')
	joindata['rpc']=request.COOKIES.get('rpc')
	joindata['c']=request.COOKIES.get('c')
	joindata['l']=request.COOKIES.get('l')
	joindata['hr']=request.COOKIES.get('hr')

	customer = [['firstname', request.COOKIES.get('fname')], 
               ['lastname', request.COOKIES.get('lname')], 
               ['email',request.COOKIES.get('email')], 
               ['mobile', request.COOKIES.get('pnumber')],
               ['country_phone_code', '+91'],
               ['title',request.COOKIES.get('initial')],
               ]
	customer_details=mydict(customer)
	payload={'fwdp':'{}','customer_details':'%s'%customer_details}
	headers = {
	'content-type': "application/x-www-form-urlencoded"
	}
	response = requests.request("POST", url, data=payload,headers=headers, params=joindata, auth=('apitesting@goibibo.com','test123'))
	print "res", response.json()	
	#print response
	#return HttpResponse(response)
	from datetime import datetime
	fmt = '%Y/%m/%d'
	print "respons", response
	print "response.json", response.json()['success']
	response1 = render_to_response("hotels/hotel-payment.html",{'response':response.json()}, context_instance=RequestContext(request))	
	response1.set_cookie('provisionalbooking_status',response.json()['success'])
	# Code for storing Order Details
	order=Order()	
	order.userprofile =UserProfile.objects.get(user=request.user)
	order.hotelcode=request.COOKIES.get('hc')
	order.hotelname=request.COOKIES.get('hn')
	order.hotelcity=request.COOKIES.get('c')
	order.checkin=datetime.strptime(request.COOKIES.get('checkin'), fmt)
	order.checkout=datetime.strptime(request.COOKIES.get('checkout'), fmt)
	order.rooms=request.COOKIES.get('rooms')
	order.guest=request.COOKIES.get('guest')
	order.save()
	response1.set_cookie('orderdetails',order.id)

	#Code for storing OrderList Details
	joindata=request.COOKIES.get('joindata')
	# print "joindata.length", len(joindata.split('-'))
	# print "joindata", joindata.split('-')
	joindata1=joindata.split('-')
	print "joindata1",joindata1
	if joindata1[4]:
		joindata4=joindata1[4].split('_')
		print "joindata1[4]",joindata4
		orderlist=OrderList()
		orderlist.order=order
		orderlist.room=1
		orderlist.adults=joindata4[0]
		orderlist.children=joindata4[1]
		orderlist.child1_age=joindata4[2]
		orderlist.child2_age=joindata4[3]
		orderlist.save()
	if (len(joindata1)==6):
		joindata5=joindata1[5].split('_')
		print "joindata1[5]",joindata5
		orderlist=OrderList()
		orderlist.order=order
		orderlist.room=2
		orderlist.adults=joindata5[0]
		orderlist.children=joindata5[1]
		orderlist.child1_age=joindata5[2]
		orderlist.child2_age=joindata5[3]
		orderlist.save()
	if (len(joindata1)==7):
		joindata6=joindata1[6].split('_')
		print "joindata1[6]",joindata6
		orderlist=OrderList()
		orderlist.order=order
		orderlist.room=3
		orderlist.adults=joindata6[0]
		orderlist.children=joindata6[1]
		orderlist.child1_age=joindata6[2]
		orderlist.child2_age=joindata6[3]
		orderlist.save()
	if (len(joindata1)==8):
		joindata7=joindata1[7].split('_')
		print "joindata1[7]",joindata7
		orderlist=OrderList()
		orderlist.order=order
		orderlist.room=4
		orderlist.adults=joindata7[0]
		orderlist.children=joindata7[1]
		orderlist.child1_age=joindata7[2]
		orderlist.child2_age=joindata7[3]
		orderlist.save()

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
	response1.set_cookie('payudetails',payudetails.id)
	response1.set_cookie('payustatus',payudetails.status)
	return response1

def confirmbooking(request):
	from django.utils import simplejson
	import urllib
	import requests
	from hashlib import md5, sha512
	guest = request.POST.get('guest')
	firstname = request.POST.get('firstname')
	amount = request.POST.get('amount')
	gobookingid = request.POST.get('gobookingid')
	udf1 = request.POST.get('udf1')
	productinfo = request.POST.get('productinfo')
	email = request.POST.get('email')
	createhash = 'test123' + gobookingid + '|'+ str(amount) + '|' + productinfo.lower()+ '|' + firstname.lower() + '|' + email + '|' + udf1 + '|'  + guest + '|' +"travelibibo"
	createhash = sha512(createhash).hexdigest()
	print createhash
	print gobookingid
	url = "http://pp.goibibobusiness.com/api/hotels/b2b/confirm_booking/"
	payload = {'secretkey':createhash, 'gobookingid':gobookingid}
	headers = {
	'content-type': "application/x-www-form-urlencoded"
	}
	response = requests.request("POST", url, data=payload,headers=headers, auth=('apitesting@goibibo.com','test123'))
	print "res", response.json()

	#Code for storing Transaction Details
	if 'data' in response.json():
		response_json=response.json()['data']
		transaction=Transaction()
		transaction.order=Order.objects.get(id=request.COOKIES.get('orderdetails'))
		transaction.payu_details=PayuDetails.objects.get(id=request.COOKIES.get('payudetails'))
		transaction.provisionalbooking_id=gobookingid
		if 'bookingid' in response_json:
			transaction.confirmationbooking_id=response_json['bookingid']
		else:
			transaction.confirmationbooking_id=''
		transaction.productinfo=productinfo
		transaction.payu_status=request.COOKIES.get('payustatus')
		transaction.provisionalbooking_status=request.COOKIES.get('provisionalbooking_status')
		transaction.confirmationbooking_status=response_json['status']
		transaction.save()

		send_templated_mail(
					template_name='bookingdetails_hotel',
					from_email='testmail123sample@gmail.com',
					recipient_list=[registration_form.cleaned_data["email"]],
					context={
						'username': registration_form.cleaned_data["email"],
						'name': registration_form.cleaned_data["first_name"],
						'bookingid':transaction.confirmationbooking_id,
						'guests':request.COOKIES.get('guest'),
						# 'amount':request.COOKIES.get('guest'),
						'checkin':request.COOKIES.get('checkin'),
						'checkout':request.COOKIES.get('checkout'),
					},
				)

	return render_to_response("hotels/hotel-book-successfull.html",{'response':response.json()}, context_instance=RequestContext(request))

def bookingstatus(request):
	return render_to_response("hotels/bookingstatus.html",context_instance=RequestContext(request))


def getbookingstatus(request):
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	# gobookingid='GOHTLDV22896e1439528786'
	gobookingid =request.POST.get('bookid',request.COOKIES.get('bookid'))
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