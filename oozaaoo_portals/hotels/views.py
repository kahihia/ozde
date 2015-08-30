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
from django.contrib import messages
import datetime
import logging
# logger = logging.getLogger(__name__)
from django.core.cache import cache


class mydict(dict):
    def __str__(self):
        return json.dumps(self)

def log_function(query, response):
	logging.basicConfig(filename='mysite.log', level=logging.INFO)
	logging.info("******************************************************************************************************")
	logging.info(datetime.datetime.now())
	logging.info(query)
	logging.info(response)
	logging.info("******************************************************************************************************")


def registration(request):
	"""
	User Registration
	"""
	
	try:
		logout(request)
		message = None
		user=User()
		userprofile=UserProfile()
		email=request.POST['email']
		if User.objects.filter(email=email).exists():
			messages.add_message(request, messages.INFO,'Email already exists')
			return HttpResponseRedirect(format_redirect_url("/register", 'error=57'))
		elif request.method == 'POST':
			
			username=request.POST['username']
			email=request.POST['email']
			password=request.POST['password']
			phone=request.POST['phone']
			dob=request.POST['dob']    
			user.is_active = True
			user.username=username
			user.email=email
			user.password=password
			user.set_password(user.password)
			user.first_name=username
			user.save()
			userprofile.user=user       
			userprofile.phone=phone
			userprofile.dateofbirth=dob
			p = UserProfile(user=user, phone=userprofile.phone, dateofbirth=userprofile.dateofbirth)
			p.save()
			message = "You have successfully completed registration."
			send_templated_mail(
					template_name='welcome',
					from_email='testmail123sample@gmail.com',
					recipient_list=user.email,
					context={
						'username': user.email,
						'name': user.first_name,})
		return render_to_response('login-register.html', {'message': "You have successfully completed registration."},
							  context_instance=RequestContext(request))
	except:
		return render_to_response('login-register.html',
								  context_instance=RequestContext(request))
							  
from django.contrib.auth import authenticate, login, logout

def login_user(request):
	"""
	Login User
	"""
	logout(request)
	username = password = ''
	print "request.POST['next']", request.POST['next']
	if request.POST["next"] != "http://localhost:8000/register/" :
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
	print user
	userprofile=UserProfile.objects.get(user_id=user.id)
	print userprofile
	return render_to_response('myprofile.html',{'user':user,'userprofile':userprofile}, context_instance=RequestContext(request))

def mybooking(request):
	user = request.user
	print user.id
	userprofile=UserProfile.objects.get(user_id=user.id)
	print userprofile.id,"userprofile"
	trans_details=Order.objects.filter(userprofile_id=userprofile.id)
	
	return render_to_response('mybooking.html',{'trans_details':trans_details}, context_instance=RequestContext(request))

def home(request):
	"""
	Home Page for Travel Portal
	"""
	from hotels.models import citylist	
	log_function('Homepage','Homepage')
	return render_to_response("hotels/home.html", context_instance=RequestContext(request))

def home_v2(request):
	"""
	Home Page for Travel Portal
	"""
	from hotels.models import citylist	
	log_function('Homepage','Homepage')
	return render_to_response("v2/portal/home_v2.html", context_instance=RequestContext(request))

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
	print "gethotellist"
	"""
	Get the hotel list based on checkin and checkout values.
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	try:
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
	except:
		messages.add_message(request, messages.INFO,'You cannot directly move to page')
		return HttpResponseRedirect(format_redirect_url("/", 'error=57'))
	try:
		if rooms4=='4':
			rooms=4
			query, getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms4, adults1, nochildrens1,childage1_1,childage2_1, adults2, nochildrens2,childage1_2,childage2_2, adults3, nochildrens3,childage1_3,childage2_3, adults4, nochildrens1,childage1_4,childage2_4,)	
		elif rooms3=='3':
			rooms=3
			query, getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms3,adults1, nochildrens1,childage1_1,childage2_1, adults2, nochildrens2,childage1_2,childage2_2, adults3, nochildrens3,childage1_3,childage2_3)
		elif rooms2=='2':
			rooms=2
			query, getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms2,adults1, nochildrens1,childage1_1,childage2_1, adults2, nochildrens2,childage1_2,childage2_2)
		else:		
			rooms=1
			query, getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms1,adults1, nochildrens1,childage1_1,childage2_1)
		try:
			cityFields = ['country']
			city = {}
			for k, v in getcityresponse['data']['city_meta_info'].iteritems():
				if k in cityFields:
					city[k] = v

			hotelFields = ['prc', 'hn', 'hr', 'hc', 'fwdp', 'c', 't', 'ibp','l','fm','offer_tag','gr']
			# hotel_city=hotelFields[5]
			# print hotel_city
			hotels = []
			for hotel in getcityresponse['data']['city_hotel_info']:
				_hotel = {}
				# _hotel = {'hn':hotel['hn']}
				for k, v in hotel.iteritems():
					if k in hotelFields:
						_hotel[k] = v
				hotels.append(_hotel)
			##################---Added by muthu---#####################
			loc_fields=['l']
			locations=set()
			for location in getcityresponse['data']['city_hotel_info']:
				for k,v in location.iteritems():
					if k in loc_fields:
						locations.add(v)

			filtered_location=list(locations)
			###########################################################
			# return HttpResponse(simplejson.dumps(hotels), mimetype='application/json')
			hotel_price = [ hotels1['prc'] for hotels1 in hotels]
			cache.set('getcityresponse', getcityresponse)
			# print "price from cache", cache.get('hotel_price')

			# for hotels1 in hotels:
			# 	print "hotels price", hotels1['prc']

				# if 'fm' in hotels:
				# 	hotel_fm=hotels.fm
				
		  	if rooms4=='4':
				joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms3)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3)+"-"+unicode(adults4)+"_"+unicode(nochildrens4)+"_"+unicode(childage1_4)+"_"+unicode(childage2_4)
				guest=int(adults1)+int(adults2)+int(adults3)+int(adults4)
				child=int(nochildrens1)+int(nochildrens2)+int(nochildrens3)+int(nochildrens4)
			elif rooms3=='3':
				joindata= unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms3)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3)
				guest=int(adults1)+int(adults2)+int(adults3)
				child=int(nochildrens1)+int(nochildrens2)+int(nochildrens3)
			elif rooms2=='2':
				joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms2)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)
				guest=int(adults1)+int(adults2)
				child=int(nochildrens1)+int(nochildrens2)
			else:
				joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms1)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)	
				guest=int(adults1)
				child=int(nochildrens1)
			response = render_to_response("hotels/hotels.html", {'city':city, 'hotels':hotels, 'joindata':joindata,'location':filtered_location}, context_instance=RequestContext(request))
			response.set_cookie( 'joindata', joindata )
		  	response.set_cookie( 'checkin', checkin )
		  	response.set_cookie( 'checkout', checkout )
		  	response.set_cookie('filterkeyword',unicode(cityid))
		  	response.set_cookie('rooms',rooms)
		  	response.set_cookie('guest',unicode(guest))
		  	response.set_cookie('child',unicode(child))
		except:
			messages.add_message(request, messages.INFO,'API not responding')
			return HttpResponseRedirect(format_redirect_url("/", 'error=57'))

	except:
		messages.add_message(request, messages.INFO,'User entered data incorrect')
		return HttpResponseRedirect(format_redirect_url("/", 'error=56'))
	log_function(query, "success:" + str(getcityresponse['success']))	
	return response

# def gethotellist_v2(request):
#     return render_to_response("v2/hotels/hotelsearch_v2.html", context_instance=RequestContext(request))
      

def gethotellist_v2(request):
	print "gethotellist_v2"
	"""
	Get the hotel list based on checkin and checkout values.
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	try:
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
	except:
		messages.add_message(request, messages.INFO,'You cannot directly move to page')
		return HttpResponseRedirect(format_redirect_url("/v2", 'error=57'))
	try:
		if rooms4=='4':
			rooms=4
			query, getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms4, adults1, nochildrens1,childage1_1,childage2_1, adults2, nochildrens2,childage1_2,childage2_2, adults3, nochildrens3,childage1_3,childage2_3, adults4, nochildrens1,childage1_4,childage2_4,)	
		elif rooms3=='3':
			rooms=3
			query, getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms3,adults1, nochildrens1,childage1_1,childage2_1, adults2, nochildrens2,childage1_2,childage2_2, adults3, nochildrens3,childage1_3,childage2_3)
		elif rooms2=='2':
			rooms=2
			query, getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms2,adults1, nochildrens1,childage1_1,childage2_1, adults2, nochildrens2,childage1_2,childage2_2)
		else:		
			rooms=1
			query, getcityresponse = GO.SearchHotelsByCity(cityid, checkinvalue, checkoutvalue,rooms1,adults1, nochildrens1,childage1_1,childage2_1)
		print "getcityresponse", getcityresponse
		try:
			cityFields = ['country']
			city = {}
			for k, v in getcityresponse['data']['city_meta_info'].iteritems():
				if k in cityFields:
					city[k] = v

			hotelFields = ['mp', 'hn', 'hr', 'hc', 'fwdp', 'c', 't', 'ibp','l','fm','offer_tag','gr']
			# hotel_city=hotelFields[5]
			# print hotel_city
			hotels = []
			for hotel in getcityresponse['data']['city_hotel_info']:
				_hotel = {}
				# _hotel = {'hn':hotel['hn']}
				for k, v in hotel.iteritems():
					if k in hotelFields:
						_hotel[k] = v
				hotels.append(_hotel)
			print "hotels", hotels
			# return HttpResponse(simplejson.dumps(hotels), mimetype='application/json')
			hotel_price = [ hotels1['mp'] for hotels1 in hotels]
			cache.set('getcityresponse', getcityresponse)
			# print "price from cache", cache.get('hotel_price')

			# for hotels1 in hotels:
			# 	print "hotels price", hotels1['prc']

				# if 'fm' in hotels:
				# 	hotel_fm=hotels.fm
				
		  	if rooms4=='4':
				joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms3)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3)+"-"+unicode(adults4)+"_"+unicode(nochildrens4)+"_"+unicode(childage1_4)+"_"+unicode(childage2_4)
				guest=int(adults1)+int(adults2)+int(adults3)+int(adults4)
				child=int(nochildrens1)+int(nochildrens2)+int(nochildrens3)+int(nochildrens4)
			elif rooms3=='3':
				joindata= unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms3)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3)
				guest=int(adults1)+int(adults2)+int(adults3)
				child=int(nochildrens1)+int(nochildrens2)+int(nochildrens3)
			elif rooms2=='2':
				joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms2)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)
				guest=int(adults1)+int(adults2)
				child=int(nochildrens1)+int(nochildrens2)
			else:
				joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms1)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)	
				guest=int(adults1)
				child=int(nochildrens1)
			response = render_to_response("v2/hotels/hotelsearch_v2.html", {'city':city, 'hotels':hotels, 'joindata':joindata}, context_instance=RequestContext(request))
			response.set_cookie( 'joindata', joindata )
		  	response.set_cookie( 'checkin', checkin )
		  	response.set_cookie( 'checkinvalue', checkinvalue )
		  	response.set_cookie( 'checkout', checkout )
		  	response.set_cookie( 'checkoutvalue', checkoutvalue )
		  	response.set_cookie('filterkeyword',unicode(cityid))
		  	response.set_cookie('rooms',rooms)
		  	response.set_cookie('guest',unicode(guest))
		  	response.set_cookie('child',unicode(child))
		except:
			messages.add_message(request, messages.INFO,'API not responding')
			return HttpResponseRedirect(format_redirect_url("/v2", 'error=57'))

	except:
		messages.add_message(request, messages.INFO,'User entered data incorrect')
		return HttpResponseRedirect(format_redirect_url("/v2", 'error=56'))
	log_function(query, "success:" + str(getcityresponse['success']))	
	return response

# def gethoteldetails_v2(request):
#     return render_to_response("v2/hotels/hoteldetails_v2.html", context_instance=RequestContext(request))

def gethoteldetails_v2(request):
	"""
	Get the hotel Details based on list IBP(v3, v6) and FWDP.
	"""		
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')			
	joindata = request.COOKIES.get('joindata')
	hc = request.POST.get('hc',request.COOKIES.get('hc'))	
	ibp = request.POST.get('ibp',request.COOKIES.get('ibp'))
	fwdp =request.POST.get('fwdp',request.COOKIES.get('fwdp'))

	from datetime import datetime
	fmt = '%Y/%m/%d'
	d0=datetime.strptime(request.COOKIES.get('checkin'), fmt)
	d1=datetime.strptime(request.COOKIES.get('checkout'), fmt)
	no_nightbook=str((d1-d0).days)	

	# try:
	query, gethoteldetailresponse = GO.getHotelDetailsByCity(joindata, hc, ibp, fwdp)
	print "gethoteldetailresponse",gethoteldetailresponse
	gethotelreviewresponse = GO.getHotelReviewsDetails(hc)
	# print "gethotelreviewresponse", gethotelreviewresponse

	# # /** Hotel  Details */
	# try:
	hoteldetails = ['prc', 'pincode', 'room_count', 'vcid', 'hn', 'address', 'c', 'des','l','hr','gr','la','lo','rooms_data']
	_hotel = {}
	for k, v in gethoteldetailresponse['data'].iteritems():		
		# _hotel = {'hn':hotel['hn']}		
		if k in hoteldetails:
			_hotel[k] = v

	# /** Hotel  Gallery Image */		
	_hotel['gallery']= gethoteldetailresponse['data']['gallery']

	hotelroominfos = []
	for hotelroominfo in gethoteldetailresponse['data']['rooms_data']:		
		# print "hotelroominfo", hotelroominfo
		_rhotelinfo = {'rtc':hotelroominfo['rtc'], 'rpc':hotelroominfo['rpc'], 'rmt':hotelroominfo['rmt']}
		hotelroominfos.append(_rhotelinfo)	
	print "hotelroominfos", hotelroominfos

	# /** Hotel  Reviews Details */		
	# hotelreviewsFields = ['hotelName', 'firstName', 'lastName', 'hotelCity', 'totalRating', 'reviewContent', 'createdAt', 'reviewTitle','attractions']	
	# reviews = []
	# for hotelreview in gethotelreviewresponse['data']:
	# 	print "hotelreview", hotelreviewt
	# 	review = {}
	# 	for f in hotelreviewsFields:
	# 		if f in hotelreview, 'mp'::t
	# 		 		review[f] = hotelreview[f]
	# 		else:
	# 				review[f] = None
	# 	reviews.append(review)
	# print "reviews","***************", reviews
	morehoteldata = {'joindata':joindata, 'hc':hc, 'ibp':ibp, 'fwdp':fwdp}
	# except:
	# 	messages.add_message(request, messages.INFO,'API not responding')
	# 	return HttpResponseRedirect(format_redirect_url("/gethotellist", 'error=54'))
	# reviews = []
	# for hotelreview in gethotelreviewresponse['data']:
	# 	_rhotel = {'hotelName':hotelreview['hotelName'], 'totalRating':hotelreview['totalRating'], 'hotelCity':hotelreview['hotelCity'], 'reviewContent':hotelreview['reviewContent'], 'firstName':hotelreview['firstName']}
	# 	reviews.append(_rhotel)
	# return HttpResponse(simplejson.dumps(hotelroominfos), mimetype='application/json')
	# response = render_to_response("hotels/hoteldetails.html", {'hotels':_hotel , 'reviews':reviews, 'morehoteldatas':morehoteldata, 'hotelroominfos':hotelroominfos }, context_instance=RequestContext(request))	
	response = render_to_response("v2/hotels/hoteldetails_v2.html", {'hotels':_hotel , 'morehoteldatas':morehoteldata, 'hotelroominfos':hotelroominfos }, context_instance=RequestContext(request))
	response.set_cookie('hc',hc)
	response.set_cookie('ibp',ibp)
	response.set_cookie('fwdp',fwdp)
	for hotelroominfo in hotelroominfos:
		response.set_cookie('rtc',hotelroominfo['rtc'])
		response.set_cookie('rpc',hotelroominfo['rpc'])
		response.set_cookie('rmt',hotelroominfo['rmt'])
	response.set_cookie('hn',_hotel['hn'])
	response.set_cookie('prc',_hotel['prc'])
	response.set_cookie('c',_hotel['c'])
	response.set_cookie('l',_hotel['l'])
	response.set_cookie('hr',_hotel['hr'])
	response.set_cookie('la',_hotel['la'])
	response.set_cookie('lo',_hotel['lo'])
	response.set_cookie('no_night', no_nightbook)
	# except:
	# 	messages.add_message(request, messages.INFO,'User entered data incorrect')
	# 	return HttpResponseRedirect(format_redirect_url("/", 'error=55'))
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
	# try:
	query, gethoteldetailresponse = GO.getHotelDetailsByCity(joindata, hc, ibp, fwdp)
	print "gethoteldetailresponse",gethoteldetailresponse
	gethotelreviewresponse = GO.getHotelReviewsDetails(hc)
	# print "gethotelreviewresponse", gethotelreviewresponse

	# # /** Hotel  Details */
	# try:
	hoteldetails = ['prc', 'pincode', 'room_count', 'vcid', 'hn', 'address', 'c', 'des','l','hr','gr','la','lo','rooms_data']
	_hotel = {}
	for k, v in gethoteldetailresponse['data'].iteritems():		
		# _hotel = {'hn':hotel['hn']}		
		if k in hoteldetails:
			_hotel[k] = v

	# /** Hotel  Gallery Image */		
	_hotel['gallery']= gethoteldetailresponse['data']['gallery']

	hotelroominfos = []
	for hotelroominfo in gethoteldetailresponse['data']['rooms_data']:		
		# print "hotelroominfo", hotelroominfo
		_rhotelinfo = {'rtc':hotelroominfo['rtc'], 'rpc':hotelroominfo['rpc']}
		hotelroominfos.append(_rhotelinfo)	
	print "hotelroominfos", hotelroominfos

	# /** Hotel  Reviews Details */		
	# hotelreviewsFields = ['hotelName', 'firstName', 'lastName', 'hotelCity', 'totalRating', 'reviewContent', 'createdAt', 'reviewTitle','attractions']	
	# reviews = []
	# for hotelreview in gethotelreviewresponse['data']:
	# 	print "hotelreview", hotelreview
	# 	review = {}
	# 	for f in hotelreviewsFields:
	# 		if f in hotelreview:
	# 		 		review[f] = hotelreview[f]
	# 		else:
	# 				review[f] = None
	# 	reviews.append(review)
	# print "reviews","***************", reviews
	morehoteldata = {'joindata':joindata, 'hc':hc, 'ibp':ibp, 'fwdp':fwdp}	
	# except:
	# 	messages.add_message(request, messages.INFO,'API not responding')
	# 	return HttpResponseRedirect(format_redirect_url("/gethotellist", 'error=54'))
	# reviews = []
	# for hotelreview in gethotelreviewresponse['data']:
	# 	_rhotel = {'hotelName':hotelreview['hotelName'], 'totalRating':hotelreview['totalRating'], 'hotelCity':hotelreview['hotelCity'], 'reviewContent':hotelreview['reviewContent'], 'firstName':hotelreview['firstName']}
	# 	reviews.append(_rhotel)
	# return HttpResponse(simplejson.dumps(hotelroominfos), mimetype='application/json')

	# response = render_to_response("hotels/hoteldetails.html", {'hotels':_hotel , 'reviews':reviews, 'morehoteldatas':morehoteldata, 'hotelroominfos':hotelroominfos }, context_instance=RequestContext(request))	
	response = render_to_response("hotels/hoteldetails.html", {'hotels':_hotel , 'morehoteldatas':morehoteldata, 'hotelroominfos':hotelroominfos }, context_instance=RequestContext(request))
	response.set_cookie('hc',hc)
	response.set_cookie('ibp',ibp)
	response.set_cookie('fwdp',fwdp)
	for hotelroominfo in hotelroominfos:
		response.set_cookie('rtc',hotelroominfo['rtc'])
		response.set_cookie('rpc',hotelroominfo['rpc'])
	response.set_cookie('hn',_hotel['hn'])
	response.set_cookie('prc',_hotel['prc'])
	response.set_cookie('c',_hotel['c'])
	response.set_cookie('l',_hotel['l'])
	response.set_cookie('hr',_hotel['hr'])
	response.set_cookie('la',_hotel['la'])
	response.set_cookie('lo',_hotel['lo'])
	# except:
	# 	messages.add_message(request, messages.INFO,'User entered data incorrect')
	# 	return HttpResponseRedirect(format_redirect_url("/", 'error=55'))
	return response
	
@login_required(login_url='/register/')
def userdetails(request):
	"""
	UserDetails for PayU Methods with Amount.
	"""	
	try:
		rtc = request.POST.get('rtc',request.COOKIES.get('rtc'))
		rpc = request.POST.get('rpc',request.COOKIES.get('rpc'))
		from datetime import datetime
		fmt = '%Y/%m/%d'
		d0=datetime.strptime(request.COOKIES.get('checkin'), fmt)
		d1=datetime.strptime(request.COOKIES.get('checkout'), fmt)
		result=str((d1-d0).days)
		print result
		response= render_to_response("hotels/hotel-booking.html",{'results':result}, context_instance=RequestContext(request))
		response.set_cookie('rtc',rtc)
		response.set_cookie('rpc',rpc)
	except:
		messages.add_message(request, messages.INFO,'Some thing went to wrong')
		print request.META.get('HTTP_REFERER','/')
		return HttpResponseRedirect(format_redirect_url(request.META.get('HTTP_REFERER','/'), 'error=53'))
	return response

def setprovisionalbooking_v2(request):	
	return render_to_response("v2/hotels/hotelpayment_v2.html", context_instance=RequestContext(request))
	
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
	print "joindata", joindata

	customer = [['firstname', request.COOKIES.get('fname')], 
               ['lastname', request.COOKIES.get('lname')], 
               ['email',request.COOKIES.get('email')], 
               ['mobile', request.COOKIES.get('pnumber')],
               ['country_phone_code', '+91'],
               ['title',request.COOKIES.get('initial')],
               ]
	customer_details=mydict(customer)
	payload={'fwdp':'{}','customer_details':'%s'%customer_details}
	print "payload", payload
	headers = {
	'content-type': "application/x-www-form-urlencoded"
	}
	# try:
	response = requests.request("POST", url, data=payload,headers=headers, params=joindata, auth=('apitesting@goibibo.com','test123'))
	print "res", response.json()	
	#print response
	#return HttpResponse(response)
	from datetime import datetime
	fmt = '%Y/%m/%d'
	print "respons", response
	print "response.json", response.json()['success']
	# response1 = render_to_response("hotels/hotel-payment.html",{'response':response.json()}, context_instance=RequestContext(request))	
	# response1.set_cookie('provisionalbooking_status',response.json()['success'])
	response1 = reverse('confirmbooking', args=[response.json()['data']['gobookingid'], response.json()['data']['udf1'], response.json()['data']['productinfo'], response.json()['data']['email']])
	return HttpResponseRedirect(response1)
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
	order.amount=request.COOKIES.get('prc')
	order.category_type="hotel"
	order.save()
	response1.set_cookie('orderdetails',order.id)

	#Code for storing OrderList Details
	joindata=request.COOKIES.get('joindata')
	joindata_split=joindata.split('-')
	print "joindata_split",joindata_split
	for i in range(4,len(joindata_split)):
		print "joindata_split", joindata_split[i]
		data = joindata_split[i].split('_')
		orderlist=OrderList()
		orderlist.order=order
		if i==4:
			orderlist.room=1
		elif i==5:
			orderlist.room=2
		elif i==6:
			orderlist.room=3
		elif i==7:
			orderlist.room=4
		elif i==8:
			orderlist.room=5	
		elif i==9:
			orderlist.room=6	
		orderlist.adults=data[0]
		orderlist.children=data[1]
		orderlist.child1_age=data[2]
		orderlist.child2_age=data[3]
		orderlist.save()

	#Code for storing PayU Details	
	payid, paystatus=store_payudetails(request)
	print "payid", payid
	print "paystatus", paystatus
	response1.set_cookie('payudetails',payid)
	response1.set_cookie('payustatus',paystatus)
	# except:
	# 	messages.add_message(request, messages.INFO,'You cannot refresh again')
	# 	return HttpResponseRedirect(format_redirect_url("/bookhotel", 'error=52'))
	# response1 = render_to_response("hotels/hotel-payment.html", context_instance=RequestContext(request))
	return response1


def confirmbooking(request, pid, udf1, pinfo, email):
	from django.utils import simplejson
	import urllib
	import requests
	from hashlib import md5, sha512
	# try:
	
	guest = request.COOKIES.get('guest')
	firstname = request.COOKIES.get('fname')
	amount = request.COOKIES.get('prc')
	# gobookingid = request.POST.get('gobookingid')
	# udf1 = request.POST.get('udf1')
	# productinfo = request.POST.get('productinfo')
	# email = request.POST.get('email')
	# guest = request.COOKIES.get('guest')
	# print "guest", guest
	# firstname = request.COOKIES.get('fname')
	# print "firstname", firstname
	# amount = request.COOKIES.get('prc')
	# print "amount", amount
	gobookingid = pid
	print "gobookingid", gobookingid
	udf1 = udf1
	print "udf1", udf1
	productinfo = pinfo
	print "productinfo", productinfo
	email = email
	print "email", email
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
					template_name='payment_hotel',
					from_email='testmail123sample@gmail.com',
					recipient_list=[request.COOKIES.get('email')],
					context={
						'user':request.COOKIES.get('fname'),
						'bookingid':transaction.confirmationbooking_id,
						'guests':request.COOKIES.get('guest'),
						# 'amount':request.COOKIES.get('guest'),
						'checkin':request.COOKIES.get('checkin'),
						'checkout':request.COOKIES.get('checkout'),
						'c':request.COOKIES.get('c'),
						'hn':request.COOKIES.get('hn'),
						'l':request.COOKIES.get('l'),
						'prc':request.COOKIES.get('prc'),
						'rooms':request.COOKIES.get('rooms'),
						'guest':request.COOKIES.get('guest'),
						'child':request.COOKIES.get('child'),
					},
				)
	# except:
	# 	messages.add_message(request, messages.INFO,'You cannot make again')
	# 	return HttpResponseRedirect(format_redirect_url("/", 'error=51'))

	return render_to_response("hotels/hotel-book-successfull.html",{'response':response.json()}, context_instance=RequestContext(request))
	# return render_to_response("hotels/hotel-book-successfull.html", context_instance=RequestContext(request))

def bookingstatus(request):
	return render_to_response("hotels/bookingstatus.html",context_instance=RequestContext(request))

def bookinginfo(request):
	return render_to_response("hotels/bookinfo.html",context_instance=RequestContext(request))

def refund(request):
	return render_to_response("hotels/refund.html",context_instance=RequestContext(request))


def getbookingstatus(request):
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	# gobookingid='GOHTLDV22896e1439528786' // working id
	gobookingid =request.POST.get('bookid')
	query,bookingstatus=GO.BookingStatus(gobookingid)
	print bookingstatus
	log_function(query, "success:" + str(bookingstatus['success']))	
	return render_to_response("hotels/bookingstatusresult.html",{'status':bookingstatus}, context_instance=RequestContext(request))
	

def getbookingdetails(request):
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	gobookingid=request.POST.get('bookid')
	#GOHTLDV2ee67a1438838485 // working id
	bookingstatus=GO.BookingDetails(gobookingid)
	try:
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
	except:
		messages.add_message(request, messages.INFO,'Your Booking Not Conformed')
		return HttpResponseRedirect(format_redirect_url("/", 'error=60'))

	# print status
	#return HttpResponse(simplejson.dumps(status), mimetype='application/json')
	return render_to_response("hotels/bookingdetail.html",{'status':status},context_instance=RequestContext(request))

def getrefund(request):
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	#gobookingid='GOHTLDV2ee67a1438838485'
	gobookingid=request.POST.get('bookid')
	getrefund=GO.RefundDetails(gobookingid)
	#return HttpResponse(simplejson.dumps(getrefund), mimetype='application/json')
	return render_to_response("hotels/refundstatus.html",{'status':getrefund['data']['refund_details']},context_instance=RequestContext(request))

def cancelhotel(request):
	return render_to_response("hotels/hotel_cancel.html",context_instance=RequestContext(request))

def confirmcancel(request):
	from django.utils import simplejson
	import urllib
	import requests
	boooingid=request.POST.get('bookid')
	url = "http://pp.goibibobusiness.com/api/hotels/b2b/confirm_cancel"
	payload = {'gobookingid':boooingid}
	print payload
	headers = {
	'content-type': "application/x-www-form-urlencoded"
	}
	response = requests.request("POST", url, data=payload,headers=headers, auth=('apitesting@goibibo.com','test123'))
	print response.json()
	#return HttpResponse(simplejson.dumps(response), mimetype='application/json')
	
	return render_to_response("hotels/conformcancel.html",{'status':response.json()},context_instance=RequestContext(request))

@csrf_exempt
def get_results_by_price(request):
	val_min=request.POST.get('val_min','1000')
	val_max=request.POST.get('val_max','10000')
	location=request.POST['location']
	star=request.POST.get('star',5)
	stars=star.split(',')
	locations=location.split(',')
	print 'locations',locations
	print 'stars',stars
	print 'val_max',val_max
	print 'val_min',val_min
	city_response = cache.get('getcityresponse')
	morevalue = []
	for values in city_response['data']['city_hotel_info']:
		if int(values['prc']) >= int(val_min) and int(values['prc']) <= int(val_max) and unicode(values['hr']) in unicode(star) and unicode(values['l']) in unicode(locations) :#or int(values['prc']) >= int(val_min) and int(values['prc']) <= int(val_max) and unicode(values['hr']) in unicode(star): #and unicode(values['fm']) in unicode(rooms):
			print'all'
			finallist = {'hotelname': values['hn'], 'hotelcode':values['hc'] ,'price': values['prc'], 'goibiborating': values['gr'], 'location': values['l'],'ibp':values['ibp'],'hotelimage':values['t'],'hotelrating':values['hr'],'fm':values['fm'],'fwdp':values['fwdp']}
			morevalue.append(finallist)
		# elif int(values['prc']) >= int(val_min) and int(values['prc']) <= int(val_max) and unicode(values['hr']) in unicode(star):#or int(values['prc']) >= int(val_min) and int(values['prc']) <= int(val_max) and unicode(values['hr']) in unicode(star): #and unicode(values['fm']) in unicode(rooms):
		# 	print'not'
		# 	finallist = {'hotelname': values['hn'], 'hotelcode':values['hc'] ,'price': values['prc'], 'goibiborating': values['gr'], 'location': values['l'],'ibp':values['ibp'],'hotelimage':values['t'],'hotelrating':values['hr'],'fm':values['fm'],'fwdp':values['fwdp']}
		# 	morevalue.append(finallist)
	# return HttpResponse(simplejson.dumps(morevalue), mimetype='application/json')
	#print 'welcome',morevalue
	return HttpResponse(simplejson.dumps(morevalue))
	
