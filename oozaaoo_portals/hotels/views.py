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

def registration_v2(request):
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
			return HttpResponseRedirect(format_redirect_url("/v2/register", 'error=1'))
		elif request.method == 'POST':
			username=request.POST['username']
			email=request.POST['email']
			password=request.POST['password']
			phone=request.POST['phone']
			dob = request.POST['dob']
			next_path=request.POST['next']
			user.is_active = True
			user.username=username
			user.email=email
			user.password=password
			user.set_password(user.password)
			user.first_name=username
			user.save()
			send_templated_mail(
					template_name='welcome',
					from_email='testmail123sample@gmail.com',
					recipient_list=[user.email],
					context=({
						'username': user.username,
						'name': user.username}))
			userprofile.user=user
			userprofile.phone=phone
			userprofile.dateofbirth=dob
			p = UserProfile(user=user, phone=userprofile.phone, dateofbirth=userprofile.dateofbirth)
			p.save()
			message = "You have successfully completed registration."
			if request.POST['next']:
				print 'yest'
				messages.add_message(request, messages.INFO,"You have successfully completed registration.")
				return HttpResponseRedirect(request.POST["next"])

			return render_to_response('v2/portal/signup_v2.html', {'message':message},context_instance=RequestContext(request))
		else:
			return render_to_response('v2/portal/signup_v2.html',context_instance=RequestContext(request))

	except:
		return render_to_response('v2/portal/signup_v2.html',
								  context_instance=RequestContext(request))

from django.contrib.auth import authenticate, login, logout

def login_user_v2(request):
	"""
	Login User
	"""
	print request.environ['HTTP_HOST']
	logout(request)
	username = password = ''
	if request.method == "POST" :
		if request.POST["next"] != request.environ['HTTP_HOST']+"/v2/register/" :
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(request.POST["next"])
			else:
				return render_to_response('v2/portal/signin_v2.html', {'msg': 'Invalid login username&password'}, context_instance=RequestContext(request))

		else:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/v2/')
	else:
		return render_to_response("v2/portal/signin_v2.html", context_instance=RequestContext(request))

def login_user(request):
	"""
	Login User
	"""
	logout(request)
	username = password = ''
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

def logout_view_v2(request):
	logout(request)
	return HttpResponseRedirect('/')

def myprofile(request):
	user = request.user

	userprofile=UserProfile.objects.get(user_id=user.id)

	return render_to_response('myprofile.html',{'user':user,'userprofile':userprofile}, context_instance=RequestContext(request))

def mybooking(request):
	try:
		user = request.user
		userprofile=UserProfile.objects.get(user_id=user.id)
		trans_details=Order.objects.filter(userprofile_id=userprofile.id)
		return render_to_response('mybooking.html',{'trans_details':trans_details}, context_instance=RequestContext(request))
	except:
		return render_to_response('mybooking.html', context_instance=RequestContext(request))
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
	return render_to_response("v2/portal/homenew_v2.html", context_instance=RequestContext(request))

def home_v3(request):
	"""
	Home Page for Travel Portal
	"""
	from hotels.models import citylist
	return render_to_response("v2/portal/home_test.html", context_instance=RequestContext(request))



def profile_v2(request):
	user = request.user
	userprofile=UserProfile.objects.get(user_id=user.id)
	trans_details=Order.objects.filter(userprofile_id=userprofile.id)
	return render_to_response("v2/portal/profile_v2.html",{'trans_details':trans_details}, context_instance=RequestContext(request))

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
	from django.conf import settings
	GO = goibiboAPI(settings.API_USERNAME, settings.API_PASSWORD)

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

	sorted_dict = OrderedDict(sorted(unsort_dict.iteritems(), key=lambda v:v[0]))
	for k, v in sorted_dict.iteritems():
		results.append(v)

	return HttpResponse(simplejson.dumps(results), mimetype='application/json')


# /** To get the Search Results based on CityId, ChecIn, Checkout, Adults, Roooms, Children **/
def gethotellist(request):
	"""
	Get the hotel list based on checkin and checkout values.
	"""

	GO = goibiboAPI(settings.API_USERNAME, settings.API_PASSWORD)

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
		return HttpResponseRedirect(format_redirect_url("/v2", 'error=11'))
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
			# for hotels1 in hotels:

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
			response = render_to_response("hotels/hotels.html", {'city':city, 'hotels':hotels, 'joindata':joindata,'locations':filtered_location}, context_instance=RequestContext(request))
			response.set_cookie( 'joindata', joindata )
			response.set_cookie( 'checkin', checkin )
			response.set_cookie( 'checkout', checkout )
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

# def gethotellist_v2(request):
#     return render_to_response("v2/hotels/hotelsearch_v2.html", context_instance=RequestContext(request))


def gethotellist_v2(request):
	"""
	Get the hotel list based on checkin and checkout values.
	"""
	from django.conf import settings
	GO = goibiboAPI(settings.API_USERNAME, settings.API_PASSWORD)

	try:
		cityid=request.POST.get('filterkeyword',request.COOKIES.get('filterkeyword'))
		checkin = request.POST.get('start',request.COOKIES.get('checkin'))
		date,month,year=checkin.split('/')
		checkinvalue = year+month+date
		checkout = request.POST.get('end',request.COOKIES.get('checkout'))
		date,month,year=checkout.split('/')
		checkoutvalue = year+month+date
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
		return HttpResponseRedirect(format_redirect_url("/v2", 'error=11'))
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

			hotelFields = ['mp', 'hn', 'hr', 'hc', 'fwdp', 'c', 't', 'ibp','l','fm','offer_tag','gr']
			# hotel_city=hotelFields[5]
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


			filtering=list(locations)
			filtered_location=filter(None,filtering)
			###########################################################

			# return HttpResponse(simplejson.dumps(hotels), mimetype='application/json')
			hotel_price = [ hotels1['mp'] for hotels1 in hotels]
			cache.set('getcityresponse', getcityresponse)

			# for hotels1 in hotels:

				# if 'fm' in hotels:
				# 	hotel_fm=hotels.fm

			if rooms4=='4':
				joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms3)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3)+"-"+unicode(adults4)+"_"+unicode(nochildrens4)+"_"+unicode(childage1_4)+"_"+unicode(childage2_4)
				guest=int(adults1)+int(adults2)+int(adults3)+int(adults4)+int(nochildrens1)+int(nochildrens2)+int(nochildrens3)+int(nochildrens4)
				child=int(nochildrens1)+int(nochildrens2)+int(nochildrens3)+int(nochildrens4)
			elif rooms3=='3':
				joindata= unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms3)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)+"-"+unicode(adults3)+"_"+unicode(nochildrens3)+"_"+unicode(childage1_3)+"_"+unicode(childage2_3)
				guest=int(adults1)+int(adults2)+int(adults3)+nt(nochildrens1)+int(nochildrens2)+int(nochildrens3)
				child=int(nochildrens1)+int(nochildrens2)+int(nochildrens3)
			elif rooms2=='2':
				joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms2)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)+"-"+unicode(adults2)+"_"+unicode(nochildrens2)+"_"+unicode(childage1_2)+"_"+unicode(childage2_2)
				guest=int(adults1)+int(adults2)+int(nochildrens1)+int(nochildrens2)
				child=int(nochildrens1)+int(nochildrens2)
			else:
				joindata = unicode(cityid)+"-"+unicode(checkinvalue)+"-"+unicode(checkoutvalue)+"-"+unicode(rooms1)+"-"+unicode(adults1)+"_"+unicode(nochildrens1)+"_"+unicode(childage1_1)+"_"+unicode(childage2_1)
				guest=int(adults1)+int(nochildrens1)
				child=int(nochildrens1)

			from datetime import datetime
			fmt = '%d/%m/%Y'
			d0=datetime.strptime(checkin, fmt)
			d1=datetime.strptime(checkout, fmt)
			no_night=str((d1-d0).days)

			date_object_checkin= datetime.strptime(checkin, '%d/%m/%Y')
 			change_datefmt_checkin=(date_object_checkin.strftime('%b %d, %Y'))

			date_object_checkout= datetime.strptime(checkout, '%d/%m/%Y')
 			change_datefmt_checkout=(date_object_checkout.strftime('%b %d, %Y'))


			response = render_to_response("v2/hotels/hotelsearch_v2.html", {'change_datefmt_checkin': change_datefmt_checkin, 'change_datefmt_checkout': change_datefmt_checkout, 'no_night':no_night, 'city':city, 'hotels':hotels, 'guest':unicode(guest), 'joindata':joindata, 'locations':filtered_location}, context_instance=RequestContext(request))
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
			return HttpResponseRedirect(format_redirect_url("/v2", 'error=12'))

	except:
		messages.add_message(request, messages.INFO,'User entered data incorrect')
		return HttpResponseRedirect(format_redirect_url("/v2", 'error=13'))
	log_function(query, "success:" + str(getcityresponse['success']))
	return response

# def gethoteldetails_v2(request):
#     return render_to_response("v2/hotels/hoteldetails_v2.html", context_instance=RequestContext(request))
@csrf_exempt
def gethoteldetails_v2(request):
	"""
	Get the hotel Details based on list IBP(v3, v6) and FWDP.

	"""
	from django.conf import settings
	GO = goibiboAPI(settings.API_USERNAME, settings.API_PASSWORD)
	joindata = request.COOKIES.get('joindata')
	if request.is_ajax():
		joindata = request.POST.get('joindata')
	hc = request.POST.get('hc',request.COOKIES.get('hc'))
	ibp = request.POST.get('ibp',request.COOKIES.get('ibp'))
	fwdp =request.POST.get('fwdp',request.COOKIES.get('fwdp'))

	from datetime import datetime
	fmt = '%d/%m/%Y'
	d0=datetime.strptime(request.COOKIES.get('checkin'), fmt)
	d1=datetime.strptime(request.COOKIES.get('checkout'), fmt)
	no_night=str((d1-d0).days)

	try:
		query, gethoteldetailresponse = GO.getHotelDetailsByCity(joindata, hc, ibp, fwdp)
		gethotelreviewresponse = GO.getHotelReviewsDetails(hc)

		# # /** Hotel  Details */
		try:
			hoteldetails = ['prc', 'pincode','facilities', 'room_count', 'vcid', 'hn', 'address', 'c', 'des','l','hr','gr','la','lo','rooms_data', 'free_cancel']
			_hotel = {}
			for k, v in gethoteldetailresponse['data'].iteritems():
				# _hotel = {'hn':hotel['hn']}
				if k in hoteldetails:
					_hotel[k] = v

			if request.is_ajax():
				return HttpResponse(simplejson.dumps(_hotel),mimetype='application/json')
			# /** Hotel  Gallery Image */
			_hotel['gallery']= gethoteldetailresponse['data']['gallery']

			# /** Am */
			for k, v in gethoteldetailresponse['data']['am'].iteritems():
				_hotel[k] = v

			hotelroominfos = []
			for hotelroominfo in gethoteldetailresponse['data']['rooms_data']:
				_rhotelinfo = {'rtc':hotelroominfo['rtc'], 'rpc':hotelroominfo['rpc'], 'mp':hotelroominfo['mp'], 'ttc':hotelroominfo['ttc'], 'tp':hotelroominfo['tp'], 'tp_alltax':hotelroominfo['tp_alltax'], 'checkintime':hotelroominfo['checkintime'], 'checkouttime':hotelroominfo['checkouttime'], 'fcdt':hotelroominfo['fcdt'], 'fc':hotelroominfo['fc']}
				hotelroominfos.append(_rhotelinfo)

			# /** Hotel  Reviews Details */
			# hotelreviewsFields = ['hotelName', 'firstName', 'lastName', 'hotelCity', 'totalRating', 'reviewContent', 'createdAt', 'reviewTitle','attractions']
			# reviews = []
			# for hotelreview in gethotelreviewresponse['data']:
			# 	review = {}
			# 	for f in hotelreviewsFields:
			# 		if f in hotelreview, 'mp'::t
			# 		 		review[f] = hotelreview[f]
			# 		else:
			# 				review[f] = None
			# 	reviews.append(review)
			morehoteldata = {'joindata':joindata, 'hc':hc, 'ibp':ibp, 'fwdp':fwdp}
		except:
		 	messages.add_message(request, messages.INFO,'API not responding')
		 	return HttpResponseRedirect(format_redirect_url("/gethotellist", 'error=14'))

		# reviews = []
		# for hotelreview in gethotelreviewresponse['data']:
		# 	_rhotel = {'hotelName':hotelreview['hotelName'], 'totalRating':hotelreview['totalRating'], 'hotelCity':hotelreview['hotelCity'], 'reviewContent':hotelreview['reviewContent'], 'firstName':hotelreview['firstName']}
		# 	reviews.append(_rhotel)
		# response = render_to_response("hotels/hoteldetails.html", {'hotels':_hotel , 'reviews':reviews, 'morehoteldatas':morehoteldata, 'hotelroominfos':hotelroominfos }, context_instance=RequestContext(request))

		response = render_to_response("v2/hotels/hoteldetails_v2.html", {'hotels':_hotel , 'morehoteldatas':morehoteldata, 'hotelroominfos':hotelroominfos,  'no_night': no_night}, context_instance=RequestContext(request))
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
		response.set_cookie('no_night', no_night)
	except:
		messages.add_message(request, messages.INFO,'User entered data incorrect')
	 	return HttpResponseRedirect(format_redirect_url("/", 'error=15'))
	return response


def gethoteldetails(request):
	"""
	Get the hotel Details based on list IBP(v3, v6) and FWDP.

	"""
	GO = goibiboAPI(settings.API_USERNAME, settings.API_PASSWORD)

	joindata = request.COOKIES.get('joindata')
	hc = request.POST.get('hc',request.COOKIES.get('hc'))
	ibp = request.POST.get('ibp',request.COOKIES.get('ibp'))
	fwdp =request.POST.get('fwdp',request.COOKIES.get('fwdp'))
	# try:
	query, gethoteldetailresponse = GO.getHotelDetailsByCity(joindata, hc, ibp, fwdp)
	gethotelreviewresponse = GO.getHotelReviewsDetails(hc)

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
		_rhotelinfo = {'rtc':hotelroominfo['rtc'], 'rpc':hotelroominfo['rpc']}
		hotelroominfos.append(_rhotelinfo)

	# /** Hotel  Reviews Details */
	# hotelreviewsFields = ['hotelName', 'firstName', 'lastName', 'hotelCity', 'totalRating', 'reviewContent', 'createdAt', 'reviewTitle','attractions']
	# reviews = []
	# for hotelreview in gethotelreviewresponse['data']:
	# 	review = {}
	# 	for f in hotelreviewsFields:
	# 		if f in hotelreview:
	# 		 		review[f] = hotelreview[f]
	# 		else:
	# 				review[f] = None
	# 	reviews.append(review)
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


# @login_required(login_url='/register/')
def userdetails_v2(request):
	"""
	UserDetails for PayU Methods with Amount for Hotel.
	"""
	try:
		srtc = request.POST.get('selectedrtc',request.COOKIES.get('srtc'))
		srpc = request.POST.get('selectedrpc',request.COOKIES.get('srpc'))
		smp = request.POST.get('mp',request.COOKIES.get('smp'))
		stp = request.POST.get('totalprice',request.COOKIES.get('stp'))
		sttc = request.POST.get('totaltax',request.COOKIES.get('sttc'))
		stpcwt = request.POST.get('totalprice_wt',request.COOKIES.get('stpcwt'))
		sroomname = request.POST.get('roomname',request.COOKIES.get('sroomname'))
		from datetime import datetime
		fmt = '%d/%m/%Y'
		d0=datetime.strptime(request.COOKIES.get('checkin'), fmt)
		d1=datetime.strptime(request.COOKIES.get('checkout'), fmt)
		result=str((d1-d0).days)
		response= render_to_response("v2/hotels/hotelpayment_v2.html",{'results':result, 'srtc':srtc, 'srpc':srpc, 'smp':smp, 'stp':stp, 'sttc':sttc, 'stpcwt': stpcwt}, context_instance=RequestContext(request))
		response.set_cookie('srtc',srtc)
		response.set_cookie('srpc',srpc)
		response.set_cookie('smp',smp)
		response.set_cookie('stp',stp)
		response.set_cookie('sttc',sttc)
		response.set_cookie('stpcwt',stpcwt)
		response.set_cookie('sroomname',sroomname)
		return response
	except:
		messages.add_message(request, messages.INFO,'Some thing went to wrong')
		return HttpResponseRedirect(format_redirect_url(request.META.get('HTTP_REFERER','/'), 'error=53'))


@login_required(login_url='/register/')
def userdetails(request):
	"""
	UserDetails for PayU Methods with Amount.
	"""
	try:
		rtc = request.POST.get('rtc',request.COOKIES.get('rtc'))
		rpc = request.POST.get('rpc',request.COOKIES.get('rpc'))
		from datetime import datetime
		fmt = '%d/%m/%Y'
		d0=datetime.strptime(request.COOKIES.get('checkin'), fmt)
		d1=datetime.strptime(request.COOKIES.get('checkout'), fmt)
		result=str((d1-d0).days)
		response= render_to_response("hotels/hotel-booking.html",{'results':result}, context_instance=RequestContext(request))
		response.set_cookie('rtc',rtc)
		response.set_cookie('rpc',rpc)
	except:
		messages.add_message(request, messages.INFO,'Some thing went to wrong')
		return HttpResponseRedirect(format_redirect_url(request.META.get('HTTP_REFERER','/'), 'error=16'))
	return response

@csrf_exempt
def setprovisionalbooking_v2(request):
	from django.utils import simplejson
	import urllib
	import requests
	try:
		url = "http://www.goibibobusiness.com/api/hotels/b2b/provisional_booking/?query=hotels-"+request.COOKIES.get('joindata')+"&hc="+request.COOKIES.get('hc')+"&ibp="+request.COOKIES.get('ibp')+"&rtc="+request.COOKIES.get('rtc')+"&rpc="+request.COOKIES.get('rpc')
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
		# try:

		response = requests.request("POST", url, data=payload,headers=headers, auth=(settings.API_USERNAME, settings.API_PASSWORD))

		#return HttpResponse(response)
		from datetime import datetime
		fmt = '%Y/%m/%d'
		response1 = render_to_response("v2/hotels/hotelprovisional_v2.html",{'response':response.json()}, context_instance=RequestContext(request))
		# response1.set_cookie('provisionalbooking_status',response.json()['success'])
		#response1 = reverse('confirmbooking', args=[response.json()['data']['gobookingid'], response.json()['data']['udf1'], response.json()['data']['productinfo'], response.json()['data']['email']])
		#return HttpResponseRedirect(response1)
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
		order.amount=request.COOKIES.get('stpcwt')
		order.category_type="hotel"
		order.save()
		response1.set_cookie('orderdetails',order.id)

		#Code for storing OrderList Details
		joindata=request.COOKIES.get('joindata')
		joindata_split=joindata.split('-')
		for i in range(4,len(joindata_split)):
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
		response1.set_cookie('payudetails',payid)
		response1.set_cookie('payustatus',paystatus)
	except:
		messages.add_message(request, messages.INFO,'You cannot refresh again')
		return HttpResponseRedirect(format_redirect_url("/bookhotel", 'error=17'))
	# response1 = render_to_response("hotels/hotel-payment.html", context_instance=RequestContext(request))
	return response1
	# return render_to_response("v2/hotels/hotelpayment_v3.html", context_instance=RequestContext(request))

@csrf_exempt
def setprovisionalbooking(request):
	from django.utils import simplejson
	import urllib
	import requests
	url = "http://www.goibibobusiness.com/api/hotels/b2b/provisional_booking/"
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
	# try:

	response = requests.request("POST", url, data=payload,headers=headers, params=joindata, auth=(settings.API_USERNAME, settings.API_PASSWORD))

	#return HttpResponse(response)
	from datetime import datetime
	fmt = '%Y/%m/%d'
	# response1 = render_to_response("hotels/hotel-payment.html",{'response':response.json()}, context_instance=RequestContext(request))
	# response1.set_cookie('provisionalbooking_status',response.json()['success'])
	#response1 = reverse('confirmbooking', args=[response.json()['data']['gobookingid'], response.json()['data']['udf1'], response.json()['data']['productinfo'], response.json()['data']['email']])
	#return HttpResponseRedirect(response1)
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
	for i in range(4,len(joindata_split)):
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
	response1.set_cookie('payudetails',payid)
	response1.set_cookie('payustatus',paystatus)
	# except:
	# 	messages.add_message(request, messages.INFO,'You cannot refresh again')
	# 	return HttpResponseRedirect(format_redirect_url("/bookhotel", 'error=52'))
	# response1 = render_to_response("hotels/hotel-payment.html", context_instance=RequestContext(request))
	return response1

def confirmbooking_v2(request):
	from django.utils import simplejson
	import urllib
	import requests
	from hashlib import md5, sha512
	try:
		guest = request.POST.get('guest')
		firstname = request.POST.get('firstname',request.COOKIES.get('fname'))
		amount = request.POST.get('amount')
		gobookingid = request.POST.get('gobookingid')
		udf1 = request.POST.get('udf1')
		productinfo = request.POST.get('productinfo')
		email = request.POST.get('email')
		createhash = 'test123' + gobookingid + '|'+ str(amount) + '|' + productinfo.lower()+ '|' + firstname.lower() + '|' + email + '|' + udf1 + '|'  + guest + '|' +"travelibibo"
		createhash = sha512(createhash).hexdigest()
		url = "http://www.goibibobusiness.com/api/hotels/b2b/confirm_booking/"
		payload = {'secretkey':createhash, 'gobookingid':gobookingid}
		headers = {
		'content-type': "application/x-www-form-urlencoded"
		}

		response = requests.request("POST", url, data=payload,headers=headers, auth=(settings.API_USERNAME, settings.API_PASSWORD))

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
							'prc':request.COOKIES.get('stpcwt'),
							'rooms':request.COOKIES.get('rooms'),
							'guest':request.COOKIES.get('guest'),
							'child':request.COOKIES.get('child'),
						},
					)
	except:
		messages.add_message(request, messages.INFO,'You cannot make again')
		return HttpResponseRedirect(format_redirect_url("/v2", 'error=18'))

	return render_to_response("v2/hotels/hotelconfirmation_v2.html",{'response':response.json()}, context_instance=RequestContext(request))


def confirmbooking(request):
	from django.utils import simplejson
	import urllib
	import requests
	from hashlib import md5, sha512
	# try:

	guest = request.POST.get('guest')
	firstname = request.POST.get('firstname',request.COOKIES.get('fname'))
	amount = request.POST.get('amount')
	# gobookingid = request.POST.get('gobookingid')
	# udf1 = request.POST.get('udf1')
	# productinfo = request.POST.get('productinfo')
	# email = request.POST.get('email')
	# guest = request.COOKIES.get('guest')
	# firstname = request.COOKIES.get('fname')
	# amount = request.COOKIES.get('prc')
	gobookingid = request.POST.get('gobookingid')
	udf1 = request.POST.get('udf1')
	productinfo = request.POST.get('productinfo')
	email = request.POST.get('email')
	createhash = 'test123' + gobookingid + '|'+ str(amount) + '|' + productinfo.lower()+ '|' + firstname.lower() + '|' + email + '|' + udf1 + '|'  + guest + '|' +"travelibibo"
	createhash = sha512(createhash).hexdigest()
	url = "http://www.goibibobusiness.com/api/hotels/b2b/confirm_booking/"
	payload = {'secretkey':createhash, 'gobookingid':gobookingid}
	headers = {
	'content-type': "application/x-www-form-urlencoded"
	}

	response = requests.request("POST", url, data=payload,headers=headers, auth=(settings.API_USERNAME, settings.API_PASSWORD))


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
						'prc':request.COOKIES.get('stpcwt'),
						'rooms':request.COOKIES.get('rooms'),
						'guest':request.COOKIES.get('guest'),
						'child':request.COOKIES.get('child'),
					},
				)
	# except:
	# 	messages.add_message(request, messages.INFO,'You cannot make again')
	# 	return HttpResponseRedirect(format_redirect_url("/", 'error=51'))

	return render_to_response("v2/hotels/hotelconfirmation_v2.html",{'response':response.json()}, context_instance=RequestContext(request))
	# return render_to_response("hotels/hotel-book-successfull.html", context_instance=RequestContext(request))

def bookingstatus(request):
	return render_to_response("hotels/bookingstatus.html",context_instance=RequestContext(request))

def bookingstatus_v2(request):
	return render_to_response("v2/hotels/bookingstatus_v2.html",context_instance=RequestContext(request))


def bookinginfo(request):
	return render_to_response("hotels/bookinfo.html",context_instance=RequestContext(request))

def refund(request):
	return render_to_response("hotels/refund.html",context_instance=RequestContext(request))


def getbookingstatus(request):

	GO = goibiboAPI(settings.API_USERNAME, settings.API_PASSWORD)

	# gobookingid='GOHTLDV22896e1439528786' // working id
	gobookingid =request.POST.get('bookid')
	query,bookingstatus=GO.BookingStatus(gobookingid)
	log_function(query, "success:" + str(bookingstatus['success']))
	return render_to_response("hotels/bookingstatusresult.html",{'status':bookingstatus}, context_instance=RequestContext(request))


def getbookingdetails(request):

	GO = goibiboAPI(settings.API_USERNAME, settings.API_PASSWORD)

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
		return HttpResponseRedirect(format_redirect_url("/v2", 'error=60'))

	#return HttpResponse(simplejson.dumps(status), mimetype='application/json')
	return render_to_response("hotels/bookingdetail.html",{'status':status},context_instance=RequestContext(request))

def getrefund(request):

	GO = goibiboAPI(settings.API_USERNAME, settings.API_PASSWORD)

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
	url = "http://www.goibibobusiness.com/api/hotels/b2b/confirm_cancel"
	payload = {'gobookingid':boooingid}
	headers = {
	'content-type': "application/x-www-form-urlencoded"
	}

	response = requests.request("POST", url, data=payload,headers=headers, auth=(settings.API_USERNAME, settings.API_PASSWORD))

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
	city_response = cache.get('getcityresponse')
	morevalue = []
	if location== 'test':
		for values in city_response['data']['city_hotel_info']:
			if int(values['prc']) >= int(val_min) and int(values['prc']) <= int(val_max) and unicode(values['hr']) in unicode(star) :#and unicode(values['l']) in unicode(locations) :#or int(values['prc']) >= int(val_min) and int(values['prc']) <= int(val_max) and unicode(values['hr']) in unicode(star): #and unicode(values['fm']) in unicode(rooms):
				finallist = {'hotelname': values['hn'], 'hotelcode':values['hc'] ,'price': values['prc'], 'goibiborating': values['gr'], 'location': values['l'],'ibp':values['ibp'],'hotelimage':values['t'],'hotelrating':values['hr'],'fm':values['fm'],'fwdp':values['fwdp']}
				morevalue.append(finallist)
	else:
		for values in city_response['data']['city_hotel_info']:
			if int(values['prc']) >= int(val_min) and int(values['prc']) <= int(val_max) and unicode(values['hr']) in unicode(star) :#or int(values['prc']) >= int(val_min) and int(values['prc']) <= int(val_max) and unicode(values['hr']) in unicode(star): #and unicode(values['fm']) in unicode(rooms):
				if unicode(values['l']) in unicode(locations):
					finallist = {'hotelname': values['hn'], 'hotelcode':values['hc'] ,'price': values['prc'], 'goibiborating': values['gr'], 'location': values['l'],'ibp':values['ibp'],'hotelimage':values['t'],'hotelrating':values['hr'],'fm':values['fm'],'fwdp':values['fwdp']}
					morevalue.append(finallist)
		# elif int(values['prc']) >= int(val_min) and int(values['prc']) <= int(val_max) and unicode(values['hr']) in unicode(star):#or int(values['prc']) >= int(val_min) and int(values['prc']) <= int(val_max) and unicode(values['hr']) in unicode(star): #and unicode(values['fm']) in unicode(rooms):
		# 	finallist = {'hotelname': values['hn'], 'hotelcode':values['hc'] ,'price': values['prc'], 'goibiborating': values['gr'], 'location': values['l'],'ibp':values['ibp'],'hotelimage':values['t'],'hotelrating':values['hr'],'fm':values['fm'],'fwdp':values['fwdp']}
		# 	morevalue.append(finallist)
	# return HttpResponse(simplejson.dumps(morevalue), mimetype='application/json')
	return HttpResponse(simplejson.dumps(morevalue))

def test_view_v2(request):


	GO = goibiboAPI(settings.API_USERNAME, settings.API_PASSWORD)

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

	cityFields = ['country']
	city = {}
	for k, v in getcityresponse['data']['city_meta_info'].iteritems():
		if k in cityFields:
			city[k] = v

	hotelFields = ['mp', 'hn', 'hr', 'hc', 'fwdp', 'c', 't', 'ibp','l','fm','offer_tag','gr']
	loc_fields=['l']
	# hotel_city=hotelFields[5]
	hotels = []
	locations=set()
	for hotel in getcityresponse['data']['city_hotel_info']:
		_hotel = {}
		# _hotel = {'hn':hotel['hn']}
		for k, v in hotel.iteritems():
			if k in hotelFields:
				_hotel[k] = v
			if k in loc_fields:
				locations.add(v)
		hotels.append(_hotel)
	filtered_location=list(locations)

	##################---Added by muthu---#####################
	# loc_fields=['l']
	# locations=set()
	# for location in getcityresponse['data']['city_hotel_info']:
	# 	for k,v in location.iteritems():
	# 		if k in loc_fields:
	# 			locations.add(v)

	# filtered_location=list(locations)
	###########################################################

	# return HttpResponse(simplejson.dumps(hotels), mimetype='application/json')
	hotel_price = [ hotels1['mp'] for hotels1 in hotels]
	cache.set('getcityresponse', getcityresponse)

	# for hotels1 in hotels:

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

	from datetime import datetime
	fmt = '%Y/%m/%d'
	d0=datetime.strptime(checkin, fmt)
	d1=datetime.strptime(checkout, fmt)
	no_night=str((d1-d0).days)

	date_object_checkin= datetime.strptime(checkin, '%Y/%m/%d')
	change_datefmt_checkin=(date_object_checkin.strftime('%b %d, %Y'))

	date_object_checkout= datetime.strptime(checkout, '%Y/%m/%d')
	change_datefmt_checkout=(date_object_checkout.strftime('%b %d, %Y'))

	response = render_to_response("v2/portal/basic.html", {'change_datefmt_checkin': change_datefmt_checkin, 'change_datefmt_checkout': change_datefmt_checkout, 'no_night':no_night, 'city':city, 'hotels':hotels, 'guest':guest, 'joindata':joindata, 'locations':filtered_location}, context_instance=RequestContext(request))
	return response


def terms_and_condition(request):
	return render_to_response('v2/portal/terms_and_conditions.html',context_instance=RequestContext(request))

def privacy(request):
	return render_to_response('v2/portal/privacy.html',context_instance=RequestContext(request))

def aboutus(request):
	return render_to_response('v2/portal/aboutus.html',context_instance=RequestContext(request))

def contactus(request):
	return render_to_response('v2/portal/contactus.html',context_instance=RequestContext(request))


@csrf_exempt
def profile_details(request):
	user = request.user
	userprofile=UserProfile.objects.get(user_id=user.id)
	if request.method=="POST":
		userprofile.dateofbirth=request.POST.get('dob')
        userprofile.gender=request.POST.get('Gender')
        userprofile.save()
    	return render_to_response("v2/portal/profile_v2.html", context_instance=RequestContext(request))

def settings(request):

	obj=User.objects.get(id=request.user.id)
	obj.password=request.POST.get('password')
	obj.set_password('obj.password')
 	obj.save()
	# user = request.user
	# user=User.objects.get(id=request.user.id)
	# if request.method=="POST":
	# 	user.username=request.POST.get('name')
	# 	user.save()
	return render_to_response("v2/portal/profile_v2.html", context_instance=RequestContext(request))
