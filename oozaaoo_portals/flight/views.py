import requests
import random
import string
import json
import datetime
import urllib
import simplejson as json
from django.utils import simplejson
from json import dumps, loads
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from templated_email import send_templated_mail
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from apiservice.views import *
from flight.models import Iata

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from urllib import unquote, urlencode, unquote_plus
from django.conf import settings
from django.utils.http import urlquote
from urllib import urlencode
from urllib import unquote_plus
from django.utils import simplejson
from django.contrib import messages
from django.core.cache import cache
from datetime import datetime
from payu.views import flight_payu
from hashlib import md5, sha512


class mydict(dict):
	"""
	This is for making json data
	"""
	def __str__(self):
		return json.dumps(self)

def iata_code(request):
	"""
	Ajax for home page iata_code(flight)
	"""
	from collections import OrderedDict
	results = []
	unsort_dict = {}
	key_loc = request.GET.get('code')
	city_lists = Iata.objects.filter(city__icontains=key_loc)

	for city_list in city_lists:
		cityname = city_list.city.strip()
		citycode = city_list.code
		country = city_list.country
		unsort_dict[cityname] = {'citycode':citycode, 'label':cityname, 'value':cityname}

	sorted_dic = OrderedDict(sorted(unsort_dict.iteritems(), key=lambda v: v[0]))
	for k, v in sorted_dic.iteritems():
		results.append(v)

	return HttpResponse(simplejson.dumps(results), mimetype='application/json')

def search_flights(request):
	"""
	Search flights based on Airport code ,date,travellers,seating class
	"""
	GO = goibiboAPI(settings.API_USERNAME, settings.API_PASSWORD)
	try:
		trip=request.POST.get('trip',request.COOKIES.get('trip'))
		startdate = request.POST.get('start',request.COOKIES.get('start'))
		date,month,year=startdate.split('/')
		departure = year+month+date
		source = request.POST.get('iata_code_source',request.COOKIES.get('s_code')).strip()
		destination = request.POST.get('iata_code_destination',request.COOKIES.get('d_code')).strip()
		adult = request.POST.get('f_adults',request.COOKIES.get('adults'))
		child = request.POST.get('f_childs',request.COOKIES.get('childs','0'))
		infant = request.POST.get('f_infants',request.COOKIES.get('infants','0'))
		s_class = request.POST.get('f_class',request.COOKIES.get('class'))
		source_city = request.POST.get('flight_source',request.COOKIES.get('s_city'))
		destination_city = request.POST.get('flight_destination',request.COOKIES.get('d_city'))
	except:
		messages.add_message(request, messages.INFO,'User Entered data Incorrect')
		return HttpResponseRedirect(format_redirect_url("/", 'error=101'))
	if 'round' in trip:
		enddate = request.POST.get('end',request.COOKIES.get('end'))
		date,month,year=enddate.split('/')
		arrival = year+month+date
		# this is return url accessing query and response from api
		query, search_flights_response = GO.SearchFlights(trip,departure,source,destination,adult,child,infant,s_class,arrival)
		# split onwardflight data and return flight data from search_flights_response
		onwardflight = search_flights_response['data']['onwardflights']
		returnflight = search_flights_response['data']['returnflights']
		if onwardflight:
			#Flights sorting based on price
			sorted_onward_flights=  sorted(onwardflight, key=lambda x: x['fare']['totalfare'])
			sorted_return_flights=  sorted(returnflight, key=lambda x: x['fare']['totalfare'])
			# Zipping for template convience
			zipped = zip(sorted_onward_flights,sorted_return_flights)
			# stored flight details in redis cache based on search queries
			# Flight row id is unique value
			caching_dict = {}
			for onwardflights,returnflights in zipped:
				if 'rowid' in onwardflights:
					rowid = onwardflights['rowid']
					caching_dict[rowid] = onwardflights
				if 'rowid' in  returnflights:
					rowid = returnflights['rowid']
					caching_dict[rowid] = returnflights
			# stored redis cache
			cache.set_many(caching_dict)
		else:
			messages.add_message(request, messages.INFO,'No Flights availble this source and destination')
			return HttpResponseRedirect(format_redirect_url("/", 'error=102'))
	else:
		query, search_flights_response = GO.SearchFlights(trip, departure,source,destination,adult,child,infant,s_class)
		onwardflight = search_flights_response['data']['onwardflights']
		if onwardflight:
			#Flights sorting based on price
			sorted_onward_flights=  sorted(onwardflight, key=lambda x: x['fare']['totalfare'])
			# stored flight details in redis cache based on search queries
			# Flight row id is unique value
			caching_dict = {}
			for onwardflights in onwardflight:
				if 'rowid' in onwardflights:
					rowid = onwardflights['rowid']
					caching_dict[rowid] = onwardflights
			# stored redis cache
			cache.set_many(caching_dict)
		else:
			messages.add_message(request, messages.INFO,'No Flights availble this source and destination')
			return HttpResponseRedirect(format_redirect_url("/", 'error=103'))
	if 'oneway' in trip:
		response = render_to_response('v2/flight/flight_search_list.html', {'flight':sorted_onward_flights,'source':source_city,'destination':destination_city,'dateofdeparture':startdate,'trip':trip,'iata_code_return':destination,'iata_code_onward':source}, context_instance=RequestContext(request))
	else:
		response = render_to_response('v2/flight/flight_search_list.html', {'flight':zipped,'source':request.POST.get('flight_source',''),'destination':request.POST.get('flight_destination',''),'dateofarrival':enddate,'dateofdeparture':startdate,'trip':trip,'iata_code_return':destination,'iata_code_onward':source}, context_instance=RequestContext(request))
		response.set_cookie('end',enddate)

	response.set_cookie( 'trip', trip)
	response.set_cookie( 'start', startdate)
	response.set_cookie( 's_code', source)
	response.set_cookie( 'd_code', destination)
	response.set_cookie( 'adults', adult)
	response.set_cookie( 'childs', child)
	response.set_cookie( 'infants', infant)
	response.set_cookie( 'class', s_class)
	response.set_cookie( 's_city', source_city)
	response.set_cookie( 'd_city', destination_city)
	return response
	#return HttpResponse(simplejson.dumps(search_flights_response), mimetype='application/json')

def flight_details(request):
	"""
	get the user information and flight repricing
	"""
	try:
		reprice_url = settings.FLIGHT_BASE+'reprice/'
		trip = request.COOKIES.get('trip')
		origin = request.COOKIES.get('s_code')
		destination = request.COOKIES.get('d_code')
		depdate = request.COOKIES.get('start')
		date,month,year=depdate.split('/')
		departure = year+'-'+month+'-'+date
		adult = request.COOKIES.get('adults')
		childs = request.COOKIES.get('childs')
		infants = request.COOKIES.get('infants')
		s_class = request.COOKIES.get('class',)
		source_city = request.COOKIES.get('s_city')
		destination_city = request.COOKIES.get('d_city',)
		onward_row_id = request.POST.get('onward_row_id',cache.get('onward_row_id'))
		cache.set('onward_row_id',onward_row_id)
		return_row_id = request.POST.get('return_row_id',cache.get('return_row_id',''))
		cache.set('return_row_id',return_row_id)
	except:
		messages.add_message(request, messages.INFO,'Local storage failed')
		return HttpResponseRedirect(format_redirect_url("/SearchFlight", 'error=104'))
	if 'round' in trip:
		try:
			# arrival data
			arridate = request.COOKIES.get('end',request.COOKIES.get('end'))
			date,month,year=arridate.split('/')
			arrival = year+'-'+month+'-'+date
			# booking data get from redis cache
			booking_data_onward = cache.get(onward_row_id)
			booking_data_return = cache.get(return_row_id)
			booking_data = [booking_data_return,booking_data_onward]
			book_data_json = json.dumps(booking_data)
			cache.set('bookingdata',book_data_json)
			#Flight fare Information
			onward_total_fare = request.POST.get('onward_total_fare',cache.get('onward_total_fare'))
			cache.set('onward_total_fare',onward_total_fare)
			return_total_fare = request.POST.get('return_total_fare',cache.get('return_total_fare'))
			cache.set('return_total_fare',return_total_fare)
			total_fare = float(onward_total_fare)+float(return_total_fare)
			cache.set('total_fare',total_fare)
			#Flight seacrh keys
			onward_search_keys = request.POST.get('onward_search_key',cache.get('onward_search_keys'))
			cache.set('onward_search_keys',onward_search_keys)
			return_search_keys = request.POST.get('return_search_key',cache.get('return_search_keys'))
			cache.set('return_search_keys',return_search_keys)
		except:
			messages.add_message(request, messages.INFO,'Local storage failed')
			return HttpResponseRedirect(format_redirect_url("/SearchFlight", 'error=105'))
		#user entered queries making json format
		querydata=json.dumps({'origin':origin,'destination':destination,'depdate':departure,'adults':adult,'infants':infants,'children':childs,'arrdate':arrival})
		cache.set('querydata',querydata)
		payload = {'fare':total_fare , 'bookingdata':'{}'.format(book_data_json),'querydata':'{}'.format(querydata),'searchKey_onward':'{}'.format(onward_search_keys),'searchKey_return':'{}'.format(return_search_keys)}
		headers = {
	        'content-type': "application/x-www-form-urlencoded"
	    }
		try:
			response = requests.request("POST", reprice_url, data=payload, headers=headers, auth=(settings.API_USERNAME, settings.API_PASSWORD))
		except:
			messages.add_message(request, messages.INFO,'Check Your Internet Connection')
			return HttpResponseRedirect(format_redirect_url("/SearchFlight", 'error=106'))

			reprice_response = response.json()
		if not reprice_response['data'].has_key('Error'):
			#return HttpResponse(simplejson.dumps(reprice_response),mimetype='application/json')
			return render_to_response('v2/flight/flight_book.html',{'reprice':reprice_response,'onward':booking_data_onward,'return':booking_data_return,}, context_instance=RequestContext(request))
		else:
			messages.add_message(request, messages.INFO,'Flight Fare amount is changed')
			return HttpResponseRedirect(format_redirect_url("/", 'error=107'))
	elif 'oneway' in trip:
		try:
			booking_data = cache.get(onward_row_id)
			booking_data_onward = [cache.get(onward_row_id)]
			book_data_json = json.dumps(booking_data_onward)
			cache.set('bookingdata',book_data_json)
			#Flight fare Information
			total_fare = float(request.POST.get('onward_total_fare',cache.get('total_fare')))
			cache.set('total_fare',total_fare)
			#Flight seacrh keys
			onward_search_keys = request.POST.get('onward_search_key',cache.get('onward_search_keys',request.COOKIES.get('onward_total_fare')))
			cache.set('onward_search_keys',onward_search_keys)
			#user search queries
			querydata=json.dumps({'origin':origin,'destination':destination,'depdate':departure,'adults':adult,'infants':infants,'children':childs})
			cache.set('querydata',querydata)
		except:
			messages.add_message(request, messages.INFO,'Local Storage failed')
			return HttpResponseRedirect(format_redirect_url("/SearchFlight", 'error=108'))
		fare =  float(total_fare)
		payload = {'fare':fare , 'bookingdata':'{}'.format(book_data_json),'querydata':'{}'.format(querydata),'searchKey_onward':'{}'.format(onward_search_keys)}
		headers = {
	        'content-type': "application/x-www-form-urlencoded",
	    }
		try:
			response = requests.request("POST", reprice_url, data=payload, headers=headers, auth=(settings.API_USERNAME, settings.API_PASSWORD))
		except:
			messages.add_message(request, messages.INFO,'Check Your Internet Connection')
			return HttpResponseRedirect(format_redirect_url("/SearchFlight", 'error=109'))

		reprice_response = response.json()
		if not reprice_response['data'].has_key('Error'):
			response = render_to_response('v2/flight/flight_book.html',{'reprice':reprice_response,'onward':booking_data}, context_instance=RequestContext(request))
			response.set_cookie('total_fare',total_fare)
			return response
		else:
			messages.add_message(request, messages.INFO,'Flight Fare amount is changed or Seats not available')
			return HttpResponseRedirect(format_redirect_url("/", 'error=110'))

def tentativebooking(request):
	"""
	Storing user infromation cache
	"""
	try:
		adult = int(request.COOKIES.get('adults'))
		childs = int(request.COOKIES.get('childs'))
		infants = int(request.COOKIES.get('infants'))
	except:
		messages.add_message(request, messages.INFO,'Please searh again')
		return HttpResponseRedirect(format_redirect_url("/", 'error=111'))
	# for key, value in request.POST.iteritems():
	if adult is not None:
		for i in range(adult):
			cache.set('adult_passanger_{}'.format(i+1),{'FirstName':'{}'.format(request.POST.get('adult_fname_{}'.format(i+1))),
													  	'eticketnumber':'',
													  	'LastName':'{}'.format(request.POST.get('adult_lname_{}'.format(i+1))),
													  	'Title':'{}'.format(request.POST.get('adult_title_{}'.format(i+1))),
													  	'DateOfBirth':'',
													  	'Type':'A'
													  	})

	if childs is not None:
		for i in range(childs):
			cache.set('child_passanger_{}'.format(i+1),{'FirstName':'{}'.format(request.POST.get('child_fname_{}'.format(i+1))),
													  	'eticketnumber':'',
													  	'LastName':'{}'.format(request.POST.get('child_lname_{}'.format(i+1))),
													  	'Title':'{}'.format(request.POST.get('child_title_{}'.format(i+1))),
													  	'DateOfBirth':'{}'.format(request.POST.get('child_age_{}'.format(i+1))),
													  	'Type':'C'
													  	})

	if infants is not None:
		for i in range(infants):
			cache.set('infant_passanger_{}'.format(i+1),{'FirstName':'{}'.format(request.POST.get('infant_fname_{}'.format(i+1))),
													  	'eticketnumber':'',
													  	'LastName':'{}'.format(request.POST.get('infant_lname_{}'.format(i+1))),
													  	'Title':'{}'.format(request.POST.get('infant_title_{}'.format(i+1))),
													  	'DateOfBirth':'{}'.format(request.POST.get('infant_age_{}'.format(i+1))),
													  	'Type':'I'
													  	})
	contactinfo={'pincode':request.POST.get('pincode'),
				 'state':request.POST.get('state'),
				 'firstname':request.POST.get('adult_fname_1'),
				 'lastname':request.POST.get('adult_lname_1'),
				 'email':request.POST.get('email'),
				 'landline':request.POST.get('landline'),
				 'mobile':request.POST.get('mobile'),
				 'address':request.POST.get('address'),
				 'city':request.POST.get('city'),
				}
	cache.set('contactinfo',contactinfo)
	return flight_payu(request.POST.get('adult_fname_1'),request.POST.get('adult_lname_1'),request.POST.get('mobile'),request.POST.get('email'),cache.get('total_fare'))

@csrf_exempt
def flight_confirm(request):
	"""
	Flight tentativebooking module(bookingdata,querydata,fare,searchKey_onward,searchKey_return,paxinfo,contactinfo)
	Flight confirmation booking
	all of get from redis cache
	"""
	if 'field9' in request.POST:
		adult = int(request.COOKIES.get('adults'))
		childs = int(request.COOKIES.get('childs'))
		infants = int(request.COOKIES.get('infants'))
		trip = request.COOKIES.get('trip')
		url = settings.FLIGHT_BASE+'book/'
		confirm_url = settings.FLIGHT_BASE+'confirm/'
		# contact info
		contactinfo = cache.get('contactinfo')
		contactinfo['payment'] = request.POST.get('issuing_bank',request.POST.get('card_type'))
		#pax info
		paxinfo = []
		for i in range(adult):
			paxinfo.append(cache.get('adult_passanger_{}'.format(i+1)))
		for i in range(childs):
			paxinfo.append(cache.get('child_passanger_{}'.format(i+1)))
		for i in range(infants):
			paxinfo.append(cache.get('infant_passanger_{}'.format(i+1)))
		#booking data
		bookingdata = cache.get('bookingdata')
		#querydata
		querydata = cache.get('querydata')
		# total fare
		fare = cache.get('total_fare')
		# search key onward
		searchKey_onward = cache.get('onward_search_keys')
		if 'round' in trip:
			# search key return
			searchKey_return = cache.get('return_search_keys')
			payload = {'fare':fare , 'bookingdata':'{}'.format(bookingdata),'querydata':'{}'.format(querydata),'searchKey_onward':searchKey_onward,'searchKey_return':searchKey_return,'contactinfo':'{}'.format(contactinfo),'paxinfo':'{}'.format(paxinfo)}
		else:
			payload = {'fare':fare , 'bookingdata':'{}'.format(bookingdata),'querydata':'{}'.format(querydata),'searchKey_onward':searchKey_onward,'contactinfo':'{}'.format(contactinfo),'paxinfo':'{}'.format(paxinfo)}

		headers = {
	        'content-type': "application/x-www-form-urlencoded",
	    }
		response = requests.request("POST", url, data=payload, headers=headers, auth=(settings.API_USERNAME, settings.API_PASSWORD))
		booking_response = response.json()
		# Confirmation Booking
		md5str = settings.PAYMENT_SALT+booking_response['data']['customReference']+'|'+str(booking_response['data']['amount'])+'|'+booking_response['data']['productinfo'].lower()+'|'+contactinfo['firstname'].lower()+'|'+contactinfo['email'].lower()+'|'+settings.AMOUNT_CRYPT+'|'+ "true" + '|' +"travelibibo"
		hash_key= sha512(md5str).hexdigest()
		confirmation_payload = {'BookingId':booking_response['data']['customReference'],'secret': hash_key }
		confirmation_response = requests.request("POST", confirm_url, data=confirmation_payload,headers=headers, auth=(settings.API_USERNAME, settings.API_PASSWORD))
		confirm_booking_response = confirmation_response.json()
		return render_to_response('v2/flight/flight_confirm.html',{'response':confirm_booking_response['data']}, context_instance=RequestContext(request))
	else:
		messages.add_message(request, messages.INFO,'You cannot directly move to this page')
		return HttpResponseRedirect(format_redirect_url("/", 'error=112'))
