import requests
import logging
import random
import string
import json
from django.utils import simplejson
from json import dumps, loads
import simplejson as json
from apiservice.views import *
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.context_processors import csrf 
from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from urllib import unquote, urlencode, unquote_plus
from django.conf import settings
from django.utils.encoding import smart_unicode, force_unicode
from django.utils.http import urlquote
from urllib import urlencode
from urllib import unquote_plus
from django.utils import simplejson as json
from django.core.context_processors import csrf 
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
import collections
from django.contrib import messages
from transaction.models import *
from payu.models import *
import time
from datetime import datetime
from templated_email import send_templated_mail
import logging
from django.core.cache import cache


class mydict(dict):
        def __str__(self):
            return json.dumps(self)


def log_function(query, response,payload='Nil'):
	logging.basicConfig(filename='mysite.log', level=logging.INFO)
	logging.info("******************************************************************************************************")
	logging.info(datetime.now())
	logging.info(query)
	logging.info(payload)
	logging.info(response)
	logging.info("******************************************************************************************************")

def search_bus_v2(request):
	"""
	Search Bus based on Source and Destination
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	source= request.POST.get('source',request.COOKIES.get('source'))
	destination=request.POST.get('destination',request.COOKIES.get('destination'))
	departure=request.POST.get('start',request.COOKIES.get('start'))
	dateofdeparture = departure.replace('/','')
	arrival=request.POST.get('end',request.COOKIES.get('end'))
	dateofarrival = departure.replace('/','')
	trip=request.POST.get('trip',request.COOKIES.get('trip'))
	try:
		query,getbusresponse=GO.Searchbus(source, destination, dateofdeparture, dateofarrival,trip)
		if 'data' in getbusresponse:
			log_function(query, "success:True")
		else:
			log_function(query, "success:False" + str(getbusresponse['Error']))
		reviews = []
		try:
			for bussearchlist in getbusresponse['data']['onwardflights']:	
				_rbuslist	= {}
				_rbuslist['businfos'] = {
					'origin':bussearchlist['origin'],
					'destination':bussearchlist['destination'],
					'BusType':bussearchlist['BusType'],
					'DepartureTime':bussearchlist['DepartureTime'],
					'duration':bussearchlist['duration'],
					'skey':bussearchlist['skey'],
					'fare':bussearchlist['fare']['totalfare'],
					'TravelsName':bussearchlist['TravelsName'],
					'ArrivalTime':bussearchlist['ArrivalTime'],
					'depdate':bussearchlist['depdate'],
					'arrdate':bussearchlist['arrdate'],
					'cancellationPolicy':bussearchlist.get('cancellationPolicy'),
					'busCondition':bussearchlist.get('busCondition'),
					'BusType':bussearchlist.get('BusType'),
				}

				if bussearchlist.get('BPPrims'):
					for morevalues in bussearchlist['BPPrims']['list']:
						_rbuslist['boardingpoints'] = {'BPId':morevalues['BPId'],'BPTime':morevalues['BPTime'], 'BPLocation':morevalues['BPLocation']}

					if bussearchlist.get('DPPrims'):
						for morevalues in bussearchlist['DPPrims']['list']:
							_rbuslist['depturepoints'] = {'DPTime':morevalues['DPTime'], 'DPLocation':morevalues['DPLocation']}
					

					if bussearchlist.get('RouteSeatTypeDetail'):
						for morevalues in bussearchlist['RouteSeatTypeDetail']['list']:
							_rbuslist['seatinfo'] = {'busCondition':morevalues['busCondition'], 'seatType':morevalues['seatType'], 'SeatsAvailable':morevalues['SeatsAvailable']}
					
					reviews.append(_rbuslist)
				else:
					reviews.append(_rbuslist)
			reviews_return = []
			for bussearchlist in getbusresponse['data']['returnflights']:	
				_rbuslist	= {}
				_rbuslist['businfos'] = {
					'origin':bussearchlist['origin'],
					'destination':bussearchlist['destination'],
					'BusType':bussearchlist['BusType'],
					'DepartureTime':bussearchlist['DepartureTime'],
					'duration':bussearchlist['duration'],
					'skey':bussearchlist['skey'],
					'fare':bussearchlist['fare']['totalfare'],
					'TravelsName':bussearchlist['TravelsName'],
					'ArrivalTime':bussearchlist['ArrivalTime'],
					'depdate':bussearchlist['depdate'],
					'arrdate':bussearchlist['arrdate'],
					'cancellationPolicy':bussearchlist.get('cancellationPolicy'),
				}

				if bussearchlist.get('BPPrims'):
					for morevalues in bussearchlist['BPPrims']['list']:
						_rbuslist['boardingpoints'] = {'BPId':morevalues['BPId'],'BPTime':morevalues['BPTime'], 'BPLocation':morevalues['BPLocation']}

					if bussearchlist.get('DPPrims'):
						for morevalues in bussearchlist['DPPrims']['list']:
							_rbuslist['depturepoints'] = {'DPTime':morevalues['DPTime'], 'DPLocation':morevalues['DPLocation']}
					

					if bussearchlist.get('RouteSeatTypeDetail'):
						for morevalues in bussearchlist['RouteSeatTypeDetail']['list']:
							_rbuslist['seatinfo'] = {'busCondition':morevalues['busCondition'], 'seatType':morevalues['seatType'], 'SeatsAvailable':morevalues['SeatsAvailable']}
					
					reviews_return.append(_rbuslist)
				else:
					reviews_return.append(_rbuslist)
			travel_fields=['TravelsName']
			travels=set()
			boardingpoint=set()
			depturepoint=set()
			for travel in getbusresponse['data']['onwardflights']:
				for k,v in travel.iteritems():
					if k in travel_fields:
						travels.add(v)
				if travel.get('BPPrims'):
					for k,v in travel.get('BPPrims').iteritems():
						for s in v:
							boardingpoint.add(s['BPLocation'])
				if travel.get('DPPrims'):
					for k,v in travel.get('DPPrims').iteritems():
						for s in v:
							depturepoint.add(s['DPLocation'])
			filtered_travels=list(travels)
			filtered_bpoint=list(boardingpoint)
			filtered_dpoint=list(depturepoint)
			cache.set('getbusresponse', getbusresponse)
		except:
			messages.add_message(request, messages.INFO,'API not responding for one way trip')
			return HttpResponseRedirect(format_redirect_url("/v2/", 'error=2'))
	except:
		messages.add_message(request, messages.INFO,'User Entering data is wrong')
		return HttpResponseRedirect(format_redirect_url("/v2/", 'error=1'))

	source = unicode(source)
	destination = unicode(destination)
	# joindata_bus = dateofdeparture+"-"+TravelsName+"-"+fare+"-"+source+"-"+destination
	#return HttpResponse(simplejson.dumps(reviews), mimetype='application/json')
	if trip=='oneway':	
		response = render_to_response('v2/bus/buslist_v2.html', {'reviews':reviews,'source':source,'destination':destination,'dateofarrival':dateofarrival,'dateofdeparture':dateofdeparture,'trip':trip,'filtered_travels':filtered_travels,'filtered_bpoint':filtered_bpoint,'filtered_dpoint':filtered_dpoint}, context_instance=RequestContext(request))
	else:
		response = render_to_response('v2/bus/buslist_v2.html', {'reviews':reviews,'reviews_return':reviews_return,'source':source,'destination':destination,'dateofarrival':dateofarrival,'dateofdeparture':dateofdeparture,'trip':trip,'filtered_travels':filtered_travels,'filtered_bpoint':filtered_bpoint,'filtered_dpoint':filtered_dpoint}, context_instance=RequestContext(request))

	response.set_cookie( 'source', source)
	response.set_cookie( 'trip', trip)
	response.set_cookie( 'destination', destination)
	response.set_cookie( 'start', departure)
	response.set_cookie( 'end', arrival)
	return response
	#return render_to_response("v2/bus/buslist_v2.html", context_instance=RequestContext(request))

def search_bus(request):
	"""
	Search Bus based on Source and Destination
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	source= request.POST.get('source',request.COOKIES.get('source'))
	destination=request.POST.get('destination',request.COOKIES.get('destination'))
	departure=request.POST.get('start',request.COOKIES.get('start'))
	dateofdeparture = departure.replace('/','')
	arrival=request.POST.get('end',request.COOKIES.get('end'))
	dateofarrival = departure.replace('/','')
	trip=request.POST.get('trip',request.COOKIES.get('trip'))
	try:
		query,getbusresponse=GO.Searchbus(source, destination, dateofdeparture, dateofarrival,trip)
		if 'data' in getbusresponse:
			log_function(query, "success:True")
		else:
			log_function(query, "success:False" + str(getbusresponse['Error']))
		reviews = []
		try:
			for bussearchlist in getbusresponse['data']['onwardflights']:	
				_rbuslist	= {}
				_rbuslist['businfos'] = {
					'origin':bussearchlist['origin'],
					'destination':bussearchlist['destination'],
					'BusType':bussearchlist['BusType'],
					'DepartureTime':bussearchlist['DepartureTime'],
					'duration':bussearchlist['duration'],
					'skey':bussearchlist['skey'],
					'fare':bussearchlist['fare']['totalfare'],
					'TravelsName':bussearchlist['TravelsName'],
					'ArrivalTime':bussearchlist['ArrivalTime'],
					'depdate':bussearchlist['depdate'],
					'arrdate':bussearchlist['arrdate'],
					'cancellationPolicy':bussearchlist.get('cancellationPolicy'),
					'busCondition':bussearchlist.get('busCondition'),
					'BusType':bussearchlist.get('BusType'),
				}

				if bussearchlist.get('BPPrims'):
					for morevalues in bussearchlist['BPPrims']['list']:
						_rbuslist['boardingpoints'] = {'BPId':morevalues['BPId'],'BPTime':morevalues['BPTime'], 'BPLocation':morevalues['BPLocation']}

					if bussearchlist.get('DPPrims'):
						for morevalues in bussearchlist['DPPrims']['list']:
							_rbuslist['depturepoints'] = {'DPTime':morevalues['DPTime'], 'DPLocation':morevalues['DPLocation']}
					

					if bussearchlist.get('RouteSeatTypeDetail'):
						for morevalues in bussearchlist['RouteSeatTypeDetail']['list']:
							_rbuslist['seatinfo'] = {'busCondition':morevalues['busCondition'], 'seatType':morevalues['seatType'], 'SeatsAvailable':morevalues['SeatsAvailable']}
					
					reviews.append(_rbuslist)
				else:
					reviews.append(_rbuslist)

			
			reviews_return = []
			for bussearchlist in getbusresponse['data']['returnflights']:	
				_rbuslist	= {}
				_rbuslist['businfos'] = {
					'origin':bussearchlist['origin'],
					'destination':bussearchlist['destination'],
					'BusType':bussearchlist['BusType'],
					'DepartureTime':bussearchlist['DepartureTime'],
					'duration':bussearchlist['duration'],
					'skey':bussearchlist['skey'],
					'fare':bussearchlist['fare']['totalfare'],
					'TravelsName':bussearchlist['TravelsName'],
					'ArrivalTime':bussearchlist['ArrivalTime'],
					'depdate':bussearchlist['depdate'],
					'arrdate':bussearchlist['arrdate'],
					'cancellationPolicy':bussearchlist.get('cancellationPolicy'),
				}

				if bussearchlist.get('BPPrims'):
					for morevalues in bussearchlist['BPPrims']['list']:
						_rbuslist['boardingpoints'] = {'BPId':morevalues['BPId'],'BPTime':morevalues['BPTime'], 'BPLocation':morevalues['BPLocation']}

					if bussearchlist.get('DPPrims'):
						for morevalues in bussearchlist['DPPrims']['list']:
							_rbuslist['depturepoints'] = {'DPTime':morevalues['DPTime'], 'DPLocation':morevalues['DPLocation']}
					

					if bussearchlist.get('RouteSeatTypeDetail'):
						for morevalues in bussearchlist['RouteSeatTypeDetail']['list']:
							_rbuslist['seatinfo'] = {'busCondition':morevalues['busCondition'], 'seatType':morevalues['seatType'], 'SeatsAvailable':morevalues['SeatsAvailable']}
					
					reviews_return.append(_rbuslist)
				else:
					reviews_return.append(_rbuslist)

		except:
			messages.add_message(request, messages.INFO,'API not responding for one way trip')
			return HttpResponseRedirect(format_redirect_url("/v2/", 'error=2'))
	except:
		messages.add_message(request, messages.INFO,'User Entering data is wrong')
		return HttpResponseRedirect(format_redirect_url("/v2/", 'error=1'))

	source = unicode(source)
	destination = unicode(destination)
	# joindata_bus = dateofdeparture+"-"+TravelsName+"-"+fare+"-"+source+"-"+destination
	#return HttpResponse(simplejson.dumps(reviews), mimetype='application/json')
	if trip=='oneway':	
		response = render_to_response('bus/bus-searchlist.html', {'reviews':reviews,'source':source,'destination':destination,'dateofarrival':dateofarrival,'dateofdeparture':dateofdeparture,'trip':trip,}, context_instance=RequestContext(request))
	else:
		response = render_to_response('bus/bus-searchlist-round.html', {'reviews':reviews,'reviews_return':reviews_return,'source':source,'destination':destination,'dateofarrival':dateofarrival,'dateofdeparture':dateofdeparture,'trip':trip,}, context_instance=RequestContext(request))

	response.set_cookie( 'source', source)
	response.set_cookie( 'trip', trip)
	response.set_cookie( 'destination', destination)
	response.set_cookie( 'start', departure)
	response.set_cookie( 'end', arrival)
	return response



@csrf_exempt	
def seat_map(request):
	"""
	Seat Map Info 
	"""
	skey=request.GET.get('skey',request.COOKIES.get('skey'))
	try:
		GO = goibiboAPI('apitesting@goibibo.com', 'test123')
		query,getbusseat=GO.Busseat(skey)
		if 'data' in getbusseat:
			log_function(query, "success:True")
		else:
			log_function(query, "success:False" + str(getbusseat['Error']))
	except:
		messages.add_message(request, messages.INFO,'Search key not given by API.skey is %s'%request.POST.get('skey',request.COOKIES.get('skey')))
		return HttpResponseRedirect(format_redirect_url("/v2/", 'error=4'))
	response = HttpResponse(simplejson.dumps(getbusseat), mimetype='application/json')
	#response= simplejson.dumps(results)
	# response= render_to_response('bus/bus-seatmapinfo.html', {'results':results}, context_instance=RequestContext(request)) 
	response.set_cookie('skey',skey)
	return response

@csrf_exempt
def seat_v2(request):
	route_type=request.POST.get('route_type')
	print 'route_type',route_type
	skey=request.POST.get('skey',request.COOKIES.get('skey'))
	arri_time_oneway=request.POST.get('arri_time',request.COOKIES.get('arri_time_oneway'))
	dept_time_oneway=request.POST.get('dept_time',request.COOKIES.get('dept_time_oneway'))
	travels_name=request.POST.get('travels_name',request.COOKIES.get('travels_name'))
	bus_type=request.POST.get('bus_type',request.COOKIES.get('bus_type'))

	seat_type=bus_type.lower().split()
	number= seat_type[-1]
	name= seat_type[:-1]
	trip=request.COOKIES.get('trip')
	
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	query,getbusseat=GO.Busseat(skey)

	if 'data' in getbusseat:
		log_function(query, "success:True")
	else:
		log_function(query, "success:False" + str(getbusseat['Error']))
	results=[]
	for k,v in getbusseat.iteritems():
		results.append(v['onwardSeats'])
		for s,i in v['onwardBPs']['GetBoardingPointsResult'].iteritems():
			results.append(i)
	if 'sleeper' in name and 'semi'in name and number=='(2+2)':
		print 'seater(2+2)'
		response= render_to_response('v2/bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'seater' in name and number=='(2+2)':
		print 'seater(2+2)'
		response= render_to_response('v2/bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'airbus' in name and number=='(2+2)':
		print 'seater(2+2)'
		response= render_to_response('v2/bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'semisleeper' in name and number=='(2+2)':
		print 'seater(2+2)'
		response= render_to_response('v2/bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'sleeper' in name and number=='(2+1)':
		print 'sleeper(2+1)'
		response= render_to_response('v2/bus/sleeper(2+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'sleeper' in name and number=='(1+1)':
		print 'sleeper(1+1)'
		response= render_to_response('v2/bus/sleeper(1+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'seater/sleeper' in name and number=='(2+1)' or 'seater' in name and'sleeper' in name and number=='(2+1)':
		print 'seater_sleeper(2+1)'
		response= render_to_response('v2/bus/seater_sleeper(2+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request))
	elif 'seater' in name or 'sleeper' in name and number=='(1+1+1)':
		print 'seater(1+1+1)'
		response= render_to_response('v2/bus/seater(1+1+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request))
	elif 'seater' in name and number=='(2+3)':
		print 'seater(2+3)'
		response= render_to_response('v2/bus/seater(2+3).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request))
	else:
		print 'default seat'
		response= render_to_response('v2/bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	
	response.set_cookie('skey',skey)
	if route_type == 'return':
		response.set_cookie('skey_return',skey)
	else:
		response.set_cookie('skey_onward',skey)
	response.set_cookie('bus_type',bus_type)
	response.set_cookie('arri_time_oneway',arri_time_oneway)
	response.set_cookie('travels_name',travels_name)
	response.set_cookie('dept_time_oneway',dept_time_oneway)
	return response


@csrf_exempt
def seat(request):
	route_type=request.POST.get('route_type')
	print 'route_type',route_type
	skey=request.POST.get('skey',request.COOKIES.get('skey'))
	bus_type=request.POST.get('bus_type',request.COOKIES.get('bus_type'))

	seat_type=bus_type.lower().split()
	number= seat_type[-1]
	name= seat_type[:-1]
	trip=request.COOKIES.get('trip')
	
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	query,getbusseat=GO.Busseat(skey)

	if 'data' in getbusseat:
		log_function(query, "success:True")
	else:
		log_function(query, "success:False" + str(getbusseat['Error']))
	results=[]
	for k,v in getbusseat.iteritems():
		results.append(v['onwardSeats'])
		for s,i in v['onwardBPs']['GetBoardingPointsResult'].iteritems():
			results.append(i)
	if 'sleeper' in name and 'semi'in name and number=='(2+2)':
		print 'seater(2+2)'
		response= render_to_response('bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'seater' in name and number=='(2+2)':
		print 'seater(2+2)'
		response= render_to_response('bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'airbus' in name and number=='(2+2)':
		print 'seater(2+2)'
		response= render_to_response('bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'semisleeper' in name and number=='(2+2)':
		print 'seater(2+2)'
		response= render_to_response('bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'sleeper' in name and number=='(2+1)':
		print 'sleeper(2+1)'
		response= render_to_response('bus/sleeper(2+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'sleeper' in name and number=='(1+1)':
		print 'sleeper(1+1)'
		response= render_to_response('bus/sleeper(1+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'seater/sleeper' in name and number=='(2+1)' or 'seater' in name and'sleeper' in name and number=='(2+1)':
		print 'seater_sleeper(2+1)'
		response= render_to_response('bus/seater_sleeper(2+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request))
	elif 'seater' in name or 'sleeper' in name and number=='(1+1+1)':
		print 'seater(1+1+1)'
		response= render_to_response('bus/seater(1+1+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request))
	elif 'seater' in name and number=='(2+3)':
		print 'seater(2+3)'
		response= render_to_response('bus/seater(2+3).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request))
	else:
		print 'else seater'
		response= render_to_response('bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	
	response.set_cookie('skey',skey)
	if route_type == 'return':
		response.set_cookie('skey_return',skey)
	else:
		response.set_cookie('skey_onward',skey)
	response.set_cookie('bus_type',bus_type)
	return response

def cancelpolicy(request):
	"""
	CancelPolicy for the Particular Bus
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	skey='x55sNj4nk-c4y5eIGdK6Kv4V8NAKn5hNfNwfAeSDMq1E-i00KtoMqjSfVHVRB-I='
	query,getcencelpolicy=GO.CancelPolicy(skey)
	if 'data' in getbusseat:
		log_function(query, "success:True")
	else:
		log_function(query, "success:False" + str(getbusseat['Error']))
	policy=[]
	for k,v in getcencelpolicy.iteritems():
		 for key in v.iteritems():
			policy.append(key)

	# return HttpResponse(simplejson.dumps(policy), mimetype='application/json')
	return render_to_response('bus/bus-cancelpolicy.html', {'policy':policy}, context_instance=RequestContext(request)) 


def bus_booking(request):	
	try:
		trip = request.COOKIES.get('trip')
		if trip=='oneway':
			totalfare=request.POST.get('totalfare')
			count_of_seat=request.POST.get('seatcount')
			selected_seats_fare=request.POST.get('seatFare')
			selected_seats_fare_split=selected_seats_fare.split(",")
			selected_seats=request.POST.get('seatNumbersList')
			selected_seats_split=selected_seats.split(",")
			bpoint=request.POST.get('boarding_point_list',request.COOKIES.get('boarding_point_list'))
			bpoint_id,bpoint_name= bpoint.split("-")
			seat_and_fare=zip(selected_seats_split,selected_seats_fare_split)
			response= render_to_response('bus/bus_booking.html',{'total_amt':totalfare,'seat':seat_and_fare,'count':count_of_seat}, context_instance=RequestContext(request)) 

		else:
			totalfare=request.POST.get('total_amount')
			print 'totalfare',totalfare
			count_of_seat=request.POST.get('seat_count_round')
			print 'count_of_seat',count_of_seat
			selected_seats_fare_onward=request.POST.get('seatFareOnward')
			print 'selected_seats_fare_onward',selected_seats_fare_onward
			selected_seats_fare_split_onward=selected_seats_fare_onward.split(",")
			print 'selected_seats_fare_split_onward',selected_seats_fare_split_onward
			selected_seats_fare_return=request.POST.get('seatFareReturn')
			print 'selected_seats_fare_return',selected_seats_fare_return
			selected_seats_fare_split_return=selected_seats_fare_return.split(",")
			print 'selected_seats_fare_split_return',selected_seats_fare_split_return
			selected_seats_onward=request.POST.get('seats_onward')
			print 'selected_seats_onward',selected_seats_onward
			selected_seats_split_onward=selected_seats_onward.split(",")
			print 'selected_seats_split_onward',selected_seats_split_onward
			selected_seats_return=request.POST.get('seats_return')
			print 'selected_seats_return',selected_seats_return
			selected_seats_split_return=selected_seats_return.split(",")
			print 'selected_seats_split_return',selected_seats_split_return
			bpoint_onward=request.POST.get('OnwardBoardingPoint')
			bpoint_id_onward,bpoint_name_onward= bpoint_onward.split("-")
			print 'bpoint_id' ,bpoint_id_onward
			print 'bpoint_name' ,bpoint_name_onward
			bpoint_return=request.POST.get('ReturnBoardingPoint')
			bpoint_id_return,bpoint_name_return= bpoint_return.split("-")
			print 'bpoint_id' ,bpoint_id_return
			print 'bpoint_name' ,bpoint_name_return
			# seat_and_fare_onward=zip(selected_seats_split_onward,selected_seats_fare_split_onward)
			# print 'seat_and_fare_onward',seat_and_fare_onward
			# seat_and_fare_return=zip(selected_seats_split_return,selected_seats_fare_split_return)
			# print 'seat_and_fare_return',seat_and_fare_return
			seat_details=zip(selected_seats_split_onward,selected_seats_fare_split_onward,selected_seats_split_return,selected_seats_fare_split_return)
			response= render_to_response('bus/bus_booking.html',{'total_amt':totalfare,'seat':seat_details,'count':count_of_seat}, context_instance=RequestContext(request)) 
		# seatdetails=request.POST.get('seat',request.COOKIES.get('seatdetails'))
		# fare , seat_name=seatdetails.split(",")
		# response.set_cookie('bpoint',bpoint)
		#response.set_cookie('seatdetails',seatdetails)
		response.set_cookie('bpoint_id_onward',bpoint_id_onward)
		response.set_cookie('bpoint_name_onward',bpoint_name_onward)
		response.set_cookie('bpoint_id_return',bpoint_id_return)
		response.set_cookie('bpoint_name_onward',bpoint_name_return)
		response.set_cookie('totalfare',totalfare)
		response.set_cookie('total_seats',count_of_seat)
		return response
	except:
		messages.add_message(request, messages.INFO,'Enter the details correct way')
		trip = request.COOKIES.get('trip')
		if trip=='oneway':	
			return HttpResponseRedirect(format_redirect_url("/v2/searchbus", 'error=8'))
		else:
			return HttpResponseRedirect(format_redirect_url("/v2/searchbus", 'error=8'))

def tentativebooking_v2(request):
	#return render_to_response("v2/bus/buspayment_v2.html", context_instance=RequestContext(request))

	# try:
	trip = request.COOKIES.get('trip')
	if trip=='oneway':
		total_amount=request.POST.get('totalfare',request.COOKIES.get('total_amount'))
		count_of_seat=request.POST.get('seatcount',request.COOKIES.get('total_seats'))
		selected_seats_fare=request.POST.get('seatFare',cache.get('selected_seats_fare'))
		cache.set('selected_seats_fare', selected_seats_fare)
		selected_seats_fare_split=selected_seats_fare.split(",")
		selected_seats=request.POST.get('seatNumbersList',cache.get('selected_seats'))
		cache.set('selected_seats', selected_seats)
		selected_seats_split=selected_seats.split(",")
		bpoint=request.POST.get('boarding_point_list',cache.get('bpoint'))
		cache.set('bpoint', bpoint)
		bpoint_id,bpoint_name= bpoint.split("-")
		seat_and_fare=zip(selected_seats_split,selected_seats_fare_split)
		response= render_to_response('v2/bus/buspayment_v2.html',{'total_amount':total_amount,'seat':seat_and_fare,'count':count_of_seat,'bpoint_name':bpoint_name,'selected_seats':selected_seats}, context_instance=RequestContext(request)) 
		response.set_cookie('total_amount',total_amount)
		response.set_cookie('total_seats',count_of_seat)
		response.set_cookie('bpoint_id',bpoint_id)
		return response

	else:
		total_amount=request.POST.get('total_amount',request.COOKIES.get('total_amount'))
		print 'total_amount',total_amount
		seat_count_round=request.POST.get('seat_count_round',request.COOKIES.get('seat_count_round'))
		print 'seat_count_round',seat_count_round
		selected_seats_fare_onward=request.POST.get('seatFareOnward',cache.get('selected_seats_fare_onward'))
		cache.set('selected_seats_fare_onward', selected_seats_fare_onward)
		print 'selected_seats_fare_onward',selected_seats_fare_onward
		selected_seats_fare_split_onward=selected_seats_fare_onward.split(",")
		print 'selected_seats_fare_split_onward',selected_seats_fare_split_onward
		selected_seats_fare_return=request.POST.get('seatFareReturn',cache.get('selected_seats_fare_return'))
		cache.set('selected_seats_fare_return', selected_seats_fare_return)
		print 'selected_seats_fare_return',selected_seats_fare_return
		selected_seats_fare_split_return=selected_seats_fare_return.split(",")
		print 'selected_seats_fare_split_return',selected_seats_fare_split_return
		selected_seats_onward=request.POST.get('seats_onward',cache.get('selected_seats_onward'))
		cache.set('selected_seats_onward', selected_seats_onward)
		print 'selected_seats_onward',selected_seats_onward
		selected_seats_split_onward=selected_seats_onward.split(",")
		print 'selected_seats_split_onward',selected_seats_split_onward
		selected_seats_return=request.POST.get('seats_return',cache.get('selected_seats_return'))
		cache.set('selected_seats_return', selected_seats_return)
		print 'selected_seats_return',selected_seats_return
		selected_seats_split_return=selected_seats_return.split(",")
		print 'selected_seats_split_return',selected_seats_split_return
		OnwardBoardingPoint=request.POST.get('OnwardBoardingPoint',cache.get('OnwardBoardingPoint'))
		cache.set('OnwardBoardingPoint', OnwardBoardingPoint)
		bpoint_id_onward,bpoint_name_onward= OnwardBoardingPoint.split("-")
		print 'bpoint_id' ,bpoint_id_onward
		print 'bpoint_name' ,bpoint_name_onward
		ReturnBoardingPoint=request.POST.get('ReturnBoardingPoint',cache.get('ReturnBoardingPoint'))
		cache.set('ReturnBoardingPoint', ReturnBoardingPoint)
		bpoint_id_return,bpoint_name_return= ReturnBoardingPoint.split("-")
		print 'bpoint_id' ,bpoint_id_return
		print 'bpoint_name' ,bpoint_name_return
		arri_time_onward=request.POST.get('arri_time_onward',request.COOKIES.get('arri_time_onward'))
		arri_time_return=request.POST.get('arri_time_return',request.COOKIES.get('arri_time_return'))
		bpoint_onward=request.POST.get('bpoint_onward',request.COOKIES.get('bpoint_onward'))
		bpoint_return=request.POST.get('bpoint_return',request.COOKIES.get('bpoint_return'))
		bus_type_onward=request.POST.get('bus_type_onward',request.COOKIES.get('bus_type_onward'))
		bus_type_return=request.POST.get('bus_type_return',request.COOKIES.get('bus_type_return'))
		dept_time_onward=request.POST.get('dept_time_onward',request.COOKIES.get('dept_time_onward'))
		dept_time_return=request.POST.get('dept_time_return',request.COOKIES.get('dept_time_return'))
		fare_onward=request.POST.get('fare_onward',request.COOKIES.get('fare_onward'))
		fare_return=request.POST.get('fare_return',request.COOKIES.get('fare_return'))
		travels_onward=request.POST.get('travels_onward',request.COOKIES.get('travels_onward'))
		travels_return=request.POST.get('travels_return',request.COOKIES.get('travels_return'))
		seat_details=zip(selected_seats_split_onward,selected_seats_fare_split_onward,selected_seats_split_return,selected_seats_fare_split_return)
		response= render_to_response('v2/bus/buspayment_v2.html',{'total_amt':total_amount,
																	'seat':seat_details,
																	'count':seat_count_round,
																	'bpoint_onward':bpoint_name_onward,
																	'bpoint_return':bpoint_name_return,
																	'arri_time_onward':arri_time_onward,
																	'arri_time_return':arri_time_return,
																	'bpoint_onward_user':bpoint_onward,
																	'bpoint_return_user':bpoint_return,
																	'bus_type_onward':bus_type_onward,
																	'bus_type_return':bus_type_return,
																	'dept_time_onward':dept_time_onward,
																	'dept_time_return':dept_time_return,
																	'fare_onward':fare_onward,
																	'fare_return':fare_return,
																	'travels_onward':travels_onward,
																	'travels_return':travels_return,
																	'selected_seats_onward':selected_seats_onward,
																	'selected_seats_split_return':selected_seats_return
																	}, context_instance=RequestContext(request)) 
		response.set_cookie('total_amount',total_amount)
		response.set_cookie('seat_count_round',seat_count_round)
		response.set_cookie('arri_time_onward',arri_time_onward)
		response.set_cookie('arri_time_return',arri_time_return)
		response.set_cookie('bpoint_onward',bpoint_onward)
		response.set_cookie('bpoint_return',bpoint_return)
		response.set_cookie('bus_type_onward',bus_type_onward)
		response.set_cookie('bus_type_return',bus_type_return)
		response.set_cookie('dept_time_onward',dept_time_onward)
		response.set_cookie('dept_time_return',dept_time_return)
		response.set_cookie('fare_onward',fare_onward)
		response.set_cookie('fare_return',fare_return)
		response.set_cookie('travels_return',travels_return)
		response.set_cookie('travels_onward',travels_onward)
		response.set_cookie('bpoint_id_onward',bpoint_id_onward)
		response.set_cookie('bpoint_id_return',bpoint_id_return)
		return response
	# except:
	# 	messages.add_message(request, messages.INFO,'Enter the details correct way')
	# 	trip = request.COOKIES.get('trip')
	# 	if trip=='oneway':	
	# 		return HttpResponseRedirect(format_redirect_url("/searchbus", 'error=8'))
	# 	else:
	# 		return HttpResponseRedirect(format_redirect_url("/searchbus", 'error=8'))

def tentativebooking(request):
	import requests
	import urllib
	from django.utils import simplejson
	skey=request.POST.get('skey',request.COOKIES.get('skey'))
	skey_onward=request.COOKIES.get('skey_onward')
	skey_return=request.COOKIES.get('skey_return')
	print 'skey',skey
	bpoint_id=request.COOKIES.get('bpoint_id')
	print 'bpoint_id',bpoint_id
	bpoint_name=request.COOKIES.get('bpoint_name')
	print 'bpoint_name',bpoint_name
	totalfare=request.COOKIES.get('totalfare')
	print 'totalfare',totalfare

	total_seat=request.COOKIES.get('total_seats')
	print 'total_seat',total_seat
	title=request.POST.get('title_1',request.COOKIES.get('title'))
	print 'title', title
	fname=request.POST.get('fname_1',request.COOKIES.get('fname'))
	lname=request.POST.get('lname_1',request.COOKIES.get('lname'))
	
	age=request.POST.get('age_1',request.COOKIES.get('age'))
	title1=request.POST.get('title_2','test')
	fname1=request.POST.get('fname_2','test')
	lname1=request.POST.get('lname_2','test')
	
	age1=request.POST.get('age_2','22')
	title2=request.POST.get('title_3','test')
	fname2=request.POST.get('fname_3','test')
	lname2=request.POST.get('lname_3','test')
	
	age2=request.POST.get('age_3','22')
	title3=request.POST.get('title_4','test')
	fname3=request.POST.get('fname_4','test')
	lname3=request.POST.get('lname_4','test')
	
	age3=request.POST.get('age_4','22')
	title4=request.POST.get('title_5','test')
	fname4=request.POST.get('fname_5','test')
	lname4=request.POST.get('lname_5','test')
	
	age4=request.POST.get('age_5','22')
	title5=request.POST.get('title_6','test')
	fname5=request.POST.get('fname_6','test')
	lname5=request.POST.get('lname_6','test')
	age5=request.POST.get('age_6','22')
	trip = request.COOKIES.get('trip')
	if trip == 'oneway':
		seat_name=request.POST.get('seat_1',request.COOKIES.get('seat'))
		seat_fare=request.POST.get('fare_1',request.COOKIES.get('fare'))
		seat_name1=request.POST.get('seat_2')
		seat_fare1=request.POST.get('fare_2')
		seat_name2=request.POST.get('seat_3')
		seat_fare2=request.POST.get('fare_3')
		seat_name3=request.POST.get('seat_4')
		seat_fare3=request.POST.get('fare_4')
		seat_name4=request.POST.get('seat_5')
		seat_fare4=request.POST.get('fare_5')
		seat_name5=request.POST.get('seat_6')
		seat_fare5=request.POST.get('fare_6')
	else:
		seat_onward_name=request.POST.get('seat_onward_1','test')
		seat_onward_fare=request.POST.get('fare_onward_1','test')
		seat_return_name=request.POST.get('seat_return_1','test')
		seat_return_fare=request.POST.get('fare_return_1','test')

		seat_onward_name1=request.POST.get('seat_onward_2','test')
		seat_onward_fare1=request.POST.get('fare_onward_2','test')
		seat_return_name1=request.POST.get('seat_return_2','test')
		seat_return_fare1=request.POST.get('fare_return_2','test')

		seat_onward_name2=request.POST.get('seat_onward_3','test')
		seat_onward_fare2=request.POST.get('fare_onward_3','test')
		seat_return_name2=request.POST.get('seat_return_3','test')
		seat_return_fare2=request.POST.get('fare_return_3','test')

		seat_onward_name3=request.POST.get('seat_onward_4','test')
		seat_onward_fare3=request.POST.get('fare_onward_4','test')
		seat_return_name3=request.POST.get('seat_return_4','test')
		seat_return_fare3=request.POST.get('fare_return_4','test')

		seat_onward_name4=request.POST.get('seat_onward_5','test')
		seat_onward_fare4=request.POST.get('fare_onward_5','test')
		seat_return_name4=request.POST.get('seat_return_5','test')
		seat_return_fare4=request.POST.get('fare_return_5','test')

		seat_onward_name5=request.POST.get('seat_onward_6','test')
		seat_onward_fare5=request.POST.get('fare_onward_6','test')
		seat_return_name5=request.POST.get('seat_return_6','test')
		seat_return_fare5=request.POST.get('fare_return_6','test')
		
	email=request.POST.get('email',request.COOKIES.get('email'))
	mobile=request.POST.get('mobile',request.COOKIES.get('mobile'))
	url = "http://pp.goibibobusiness.com/api/bus/hold/"
	if trip == 'oneway':
		if total_seat == '6':
			bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_name3+"_"+fname3+"_"+lname3+"_"+age3+"-5_"+seat_name4+"_"+fname4+"_"+lname4+"_"+age4+"-6_"+seat_name5+"_"+fname5+"_"+lname5+"_"+age5
			customer1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_name],['seatFare',seat_fare]]
			customer2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_name1],['seatFare',seat_fare1]]
			customer3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_name2],['seatFare',seat_fare2]]
			customer4 = [['title', 'Mr'],['firstName', fname3],['lastName',lname3],['age',age3],['eMail',email],['mobile',mobile],['seatName', seat_name3],['seatFare',seat_fare3]]
			customer5 = [['title', 'Mr'],['firstName', fname4],['lastName',lname4],['age',age4],['eMail',email],['mobile',mobile],['seatName', seat_name4],['seatFare',seat_fare4]]
			customer6 = [['title', 'Mr'],['firstName', fname5],['lastName',lname5],['age',age5],['eMail',email],['mobile',mobile],['seatName', seat_name5],['seatFare',seat_fare5]]
			customer_details=[mydict(customer1),mydict(customer2),mydict(customer3),mydict(customer4),mydict(customer5),mydict(customer6)]

		elif total_seat == '5':
			bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_name3+"_"+fname3+"_"+lname3+"_"+age3+"-5_"+seat_name4+"_"+fname4+"_"+lname4+"_"+age4
			customer1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_name],['seatFare',seat_fare]]
			customer2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_name1],['seatFare',seat_fare1]]
			customer3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_name2],['seatFare',seat_fare2]]
			customer4 = [['title', 'Mr'],['firstName', fname3],['lastName',lname3],['age',age3],['eMail',email],['mobile',mobile],['seatName', seat_name3],['seatFare',seat_fare3]]
			customer5 = [['title', 'Mr'],['firstName', fname4],['lastName',lname4],['age',age4],['eMail',email],['mobile',mobile],['seatName', seat_name4],['seatFare',seat_fare4]]
			customer_details=[mydict(customer1),mydict(customer2),mydict(customer3),mydict(customer4),mydict(customer5)]

		elif total_seat == '4':
			bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_name3+"_"+fname3+"_"+lname3+"_"+age3
			customer1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_name],['seatFare',seat_fare]]
			customer2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_name1],['seatFare',seat_fare1]]
			customer3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_name2],['seatFare',seat_fare2]]
			customer4 = [['title', 'Mr'],['firstName', fname3],['lastName',lname3],['age',age3],['eMail',email],['mobile',mobile],['seatName', seat_name3],['seatFare',seat_fare3]]
			customer_details=[mydict(customer1),mydict(customer2),mydict(customer3),mydict(customer4)]

		elif total_seat == '3':
			bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_name2+"_"+fname2+"_"+lname2+"_"+age2
			customer1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_name],['seatFare',seat_fare]]
			customer2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_name1],['seatFare',seat_fare1]]
			customer3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_name2],['seatFare',seat_fare2]]
			customer_details=[mydict(customer1),mydict(customer2),mydict(customer3)]

		elif total_seat == '2':
			print '2'
			bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_name1+"_"+fname1+"_"+lname1+"_"+age1
			customer1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_name],['seatFare',seat_fare]]
			customer2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_name1],['seatFare',seat_fare1]]
			customer_details=[mydict(customer1),mydict(customer2)]
		else:
			bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age
			customer1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_name],['seatFare',seat_fare]]
			customer_details=[mydict(customer1)]
		print bus_join_data
		#customer = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_name],['seatFare',seat_fare]]
		print 'customer_details',customer_details
		bus=[['skey',request.COOKIES.get('skey')],
			['bp',request.COOKIES.get('bpoint_id')],
			['seats',customer_details]]
		bus_info=mydict(bus)
		onw=[['onw',bus_info]]
		onw_info=mydict(onw)
		payload={'holddata':'%s'%onw_info}
		print payload
	else:
		if total_seat == '6':
			bus_join_data_onward="1_"+seat_onward_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_onward_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_onward_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_onward_name3+"_"+fname3+"_"+lname3+"_"+age3+"-5_"+seat_onward_name4+"_"+fname4+"_"+lname4+"_"+age4+"-6_"+seat_onward_name5+"_"+fname5+"_"+lname5+"_"+age5
			bus_join_data_return="1_"+seat_return_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_return_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_return_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_return_name3+"_"+fname3+"_"+lname3+"_"+age3+"-5_"+seat_return_name4+"_"+fname4+"_"+lname4+"_"+age4+"-6_"+seat_return_name5+"_"+fname5+"_"+lname5+"_"+age5
			customer_onward_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_onward_name],['seatFare',seat_onward_fare]]
			customer_onward_2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_onward_name1],['seatFare',seat_onward_fare1]]
			customer_onward_3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_onward_name2],['seatFare',seat_onward_fare2]]
			customer_onward_4 = [['title', 'Mr'],['firstName', fname3],['lastName',lname3],['age',age3],['eMail',email],['mobile',mobile],['seatName', seat_onward_name3],['seatFare',seat_onward_fare3]]
			customer_onward_5 = [['title', 'Mr'],['firstName', fname4],['lastName',lname4],['age',age4],['eMail',email],['mobile',mobile],['seatName', seat_onward_name4],['seatFare',seat_onward_fare4]]
			customer_onward_6 = [['title', 'Mr'],['firstName', fname5],['lastName',lname5],['age',age5],['eMail',email],['mobile',mobile],['seatName', seat_onward_name5],['seatFare',seat_onward_fare5]]
			customer_return_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_return_name],['seatFare',seat_return_fare]]
			customer_return_2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_return_name1],['seatFare',seat_return_fare1]]
			customer_return_3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_return_name2],['seatFare',seat_return_fare2]]
			customer_return_4 = [['title', 'Mr'],['firstName', fname3],['lastName',lname3],['age',age3],['eMail',email],['mobile',mobile],['seatName', seat_return_name3],['seatFare',seat_return_fare3]]
			customer_return_5 = [['title', 'Mr'],['firstName', fname4],['lastName',lname4],['age',age4],['eMail',email],['mobile',mobile],['seatName', seat_return_name4],['seatFare',seat_return_fare4]]
			customer_return_6 = [['title', 'Mr'],['firstName', fname5],['lastName',lname5],['age',age5],['eMail',email],['mobile',mobile],['seatName', seat_return_name5],['seatFare',seat_return_fare5]]
			customer_onward_details=[mydict(customer_onward_1),mydict(customer_onward_2),mydict(customer_onward_3),mydict(customer_onward_4),mydict(customer_onward_5),mydict(customer_onward_6)]
			customer_return_details=[mydict(customer_return_1),mydict(customer_return_2),mydict(customer_return_3),mydict(customer_return_4),mydict(customer_return_5),mydict(customer_return_6)]

		elif total_seat == '5':
			bus_join_data_onward="1_"+seat_onward_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_onward_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_onward_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_onward_name3+"_"+fname3+"_"+lname3+"_"+age3+"-5_"+seat_onward_name4+"_"+fname4+"_"+lname4+"_"+age4
			bus_join_data_return="1_"+seat_return_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_return_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_return_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_return_name3+"_"+fname3+"_"+lname3+"_"+age3+"-5_"+seat_return_name4+"_"+fname4+"_"+lname4+"_"+age4
			customer_onward_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_onward_name],['seatFare',seat_onward_fare]]
			customer_onward_2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_onward_name1],['seatFare',seat_onward_fare1]]
			customer_onward_3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_onward_name2],['seatFare',seat_onward_fare2]]
			customer_onward_4 = [['title', 'Mr'],['firstName', fname3],['lastName',lname3],['age',age3],['eMail',email],['mobile',mobile],['seatName', seat_onward_name3],['seatFare',seat_onward_fare3]]
			customer_onward_5 = [['title', 'Mr'],['firstName', fname4],['lastName',lname4],['age',age4],['eMail',email],['mobile',mobile],['seatName', seat_onward_name4],['seatFare',seat_onward_fare4]]
			customer_return_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_return_name],['seatFare',seat_return_fare]]
			customer_return_2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_return_name1],['seatFare',seat_return_fare1]]
			customer_return_3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_return_name2],['seatFare',seat_return_fare2]]
			customer_return_4 = [['title', 'Mr'],['firstName', fname3],['lastName',lname3],['age',age3],['eMail',email],['mobile',mobile],['seatName', seat_return_name3],['seatFare',seat_return_fare3]]
			customer_return_5 = [['title', 'Mr'],['firstName', fname4],['lastName',lname4],['age',age4],['eMail',email],['mobile',mobile],['seatName', seat_return_name4],['seatFare',seat_return_fare4]]
			customer_onward_details=[mydict(customer_onward_1),mydict(customer_onward_2),mydict(customer_onward_3),mydict(customer_onward_4),mydict(customer_onward_5)]
			customer_return_details=[mydict(customer_return_1),mydict(customer_return_2),mydict(customer_return_3),mydict(customer_return_4),mydict(customer_return_5)]

		elif total_seat == '4':
			bus_join_data_onward="1_"+seat_onward_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_onward_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_onward_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_onward_name3+"_"+fname3+"_"+lname3+"_"+age3
			bus_join_data_return="1_"+seat_return_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_return_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_return_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_return_name3+"_"+fname3+"_"+lname3+"_"+age3
			customer_onward_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_onward_name],['seatFare',seat_onward_fare]]
			customer_onward_2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_onward_name1],['seatFare',seat_onward_fare1]]
			customer_onward_3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_onward_name2],['seatFare',seat_onward_fare2]]
			customer_onward_4 = [['title', 'Mr'],['firstName', fname3],['lastName',lname3],['age',age3],['eMail',email],['mobile',mobile],['seatName', seat_onward_name3],['seatFare',seat_onward_fare3]]
			customer_return_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_return_name],['seatFare',seat_return_fare]]
			customer_return_2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_return_name1],['seatFare',seat_return_fare1]]
			customer_return_3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_return_name2],['seatFare',seat_return_fare2]]
			customer_return_4 = [['title', 'Mr'],['firstName', fname3],['lastName',lname3],['age',age3],['eMail',email],['mobile',mobile],['seatName', seat_return_name3],['seatFare',seat_return_fare3]]
			customer_onward_details=[mydict(customer_onward_1),mydict(customer_onward_2),mydict(customer_onward_3),mydict(customer_onward_4)]
			customer_return_details=[mydict(customer_return_1),mydict(customer_return_2),mydict(customer_return_3),mydict(customer_return_4)]

		elif total_seat == '3':
			bus_join_data_onward="1_"+seat_onward_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_onward_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_onward_name2+"_"+fname2+"_"+lname2+"_"+age2
			bus_join_data_return="1_"+seat_return_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_return_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_return_name2+"_"+fname2+"_"+lname2+"_"+age2
			customer_onward_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_onward_name],['seatFare',seat_onward_fare]]
			customer_onward_2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_onward_name1],['seatFare',seat_onward_fare1]]
			customer_onward_3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_onward_name2],['seatFare',seat_onward_fare2]]
			customer_return_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_return_name],['seatFare',seat_return_fare]]
			customer_return_2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_return_name1],['seatFare',seat_return_fare1]]
			customer_return_3 = [['title', 'Mr'],['firstName', fname2],['lastName',lname2],['age',age2],['eMail',email],['mobile',mobile],['seatName', seat_return_name2],['seatFare',seat_return_fare2]]
			customer_onward_details=[mydict(customer_onward_1),mydict(customer_onward_2),mydict(customer_onward_3)]
			customer_return_details=[mydict(customer_return_1),mydict(customer_return_2),mydict(customer_return_3)]

		elif total_seat == '2':
			bus_join_data_onward="1_"+seat_onward_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_onward_name1+"_"+fname1+"_"+lname1+"_"+age1
			bus_join_data_return="1_"+seat_return_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_return_name1+"_"+fname1+"_"+lname1+"_"+age1
			customer_onward_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_onward_name],['seatFare',seat_onward_fare]]
			customer_onward_2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_onward_name1],['seatFare',seat_onward_fare1]]
			customer_return_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_return_name],['seatFare',seat_return_fare]]
			customer_return_2 = [['title', 'Mr'],['firstName', fname1],['lastName',lname1],['age',age1],['eMail',email],['mobile',mobile],['seatName', seat_return_name1],['seatFare',seat_return_fare1]]
			customer_onward_details=[mydict(customer_onward_1),mydict(customer_onward_2)]
			customer_return_details=[mydict(customer_return_1),mydict(customer_return_2)]
		else:
			bus_join_data_onward="1_"+seat_onward_name+"_"+fname+"_"+lname+"_"+age
			bus_join_data_return="1_"+seat_return_name+"_"+fname+"_"+lname+"_"+age
			customer_onward_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_onward_name],['seatFare',seat_onward_fare]]
			customer_return_1 = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_return_name],['seatFare',seat_return_fare]]
			customer_onward_details=[mydict(customer_onward_1)]
			customer_return_details=[mydict(customer_return_1)]
		#print bus_join_data
		#customer = [['title', 'Mr'],['firstName', fname],['lastName',lname],['age',age],['eMail',email],['mobile',mobile],['seatName', seat_name],['seatFare',seat_fare]]
		#print 'customer_details',customer_details
		bus_onward=[['skey',request.COOKIES.get('skey_onward')],
			['bp',request.COOKIES.get('bpoint_id_onward')],
			['seats',customer_onward_details]]
		bus_return=[['skey',request.COOKIES.get('skey_return')],
			['bp',request.COOKIES.get('bpoint_id_return')],
			['seats',customer_return_details]]
		bus_info_onw=mydict(bus_onward) #onw= onward
		bus_info_ret=mydict(bus_return) #ret = return
		onw=[['onw',bus_info_onw],['ret',bus_info_ret]]
		onw_info=mydict(onw)
		payload={'holddata':'%s'%onw_info}
		print payload

	
	#payload={'holddata':'{"onw":{"skey":"zJ5yLDs6ptU20KB7EtLDKv4V6NMMmZNKNqDi0J5O-msWyzc9Eww-7nLdgbubveJxLR_t0-R8Lg==","bp":"66677","seats":[{"title":"Mr","firstName":"test","lastName":"test","age":"34","eMail":"goibibobusinesstest@gmail.com","mobile":"9888888888","seatName":"36","seatFare":"122"}]}}'}
	headers = {
        'content-type': "application/x-www-form-urlencoded"
    }
	details = requests.request("POST", url, data=payload, headers=headers, auth=('apitesting@goibibo.com','test123'))
	
	#response=HttpResponse(details)
	# return HttpResponse(simplejson.dumps(response), mimetype='application/json')
	response=HttpResponseRedirect("/bus_payu/")#,{'response':response,'joindata_bus':joindata_bus}
	print details.json()
	temp= details.json()
	if temp.has_key("data"):
		log_function('http://pp.goibibobusiness.com/api/bus/hold/', "success:True"+str(details.json()['data']),payload)
	else:
		log_function('http://pp.goibibobusiness.com/api/bus/hold/', "success:False" + str(details.json()['Error']),payload)
	try:
		response.set_cookie('bookid',details.json()['data']['bookingID'])
	except:
		if temp.has_key("data"):
			messages.add_message(request, messages.INFO,temp['data']['error']+'.Please Search again')
		else:
			messages.add_message(request, messages.INFO,temp['Error']+'.Please Search again')
		return HttpResponseRedirect(format_redirect_url("/v2/bus_booking", 'error=11'))
	response.set_cookie('fname',fname)
	response.set_cookie('lname',lname)
	response.set_cookie('age',age)
	response.set_cookie('email',email)
	response.set_cookie('mobile',mobile)
	#response.set_cookie('bus_join_data',bus_join_data)

	# Code for storing Order Details
	fmt = '%Y/%m/%d'
	order=Order()	
	order.userprofile =UserProfile.objects.get(user_id=request.user.id)
	order.trip=request.COOKIES.get('trip')
	order.source=request.COOKIES.get('source')
	order.destination=request.COOKIES.get('destination')
	print 'start date',request.COOKIES.get('start')
	order.start_date=datetime.strptime(request.COOKIES.get('start'), fmt)

	if not order.trip == "oneway":
		order.end_date=datetime.strptime(request.COOKIES.get('end'), fmt)
	order.totalseats=request.COOKIES.get('total_seats')
	order.boardingpoint_id=request.COOKIES.get('bpoint_id')
	order.boardingpoint_name=request.COOKIES.get('bpoint_name')
	order.amount=request.COOKIES.get('totalfare')
	order.category_type="bus"
	order.save()
	response.set_cookie('orderdetails',order.id)
	response.set_cookie('category_type',order.category_type)

	#Code for storing OrderList Details
	if trip=='oneway':
		bus_join_data_split=bus_join_data.split('-')
		print "bus_join_data_split", bus_join_data_split
		for i in range(0,len(bus_join_data_split)):
			print "bus_join_data_split", bus_join_data_split[i]
			data = bus_join_data_split[i].split('_')
			orderlist=OrderList()
			orderlist.order=order
			orderlist.seatnumber=data[1]
			orderlist.firstname=data[2]
			orderlist.lastname=data[3]
			orderlist.age=data[4]
			orderlist.save()
	else:
		bus_join_data_split_onward=bus_join_data_onward.split('-')
		print "bus_join_data_split", bus_join_data_split_onward
		for i in range(0,len(bus_join_data_split_onward)):
			print "bus_join_data_split", bus_join_data_split_onward[i]
			data = bus_join_data_split_onward[i].split('_')
			orderlist=OrderList()
			orderlist.order=order
			orderlist.seatnumber=data[1]
			orderlist.firstname=data[2]
			orderlist.lastname=data[3]
			orderlist.age=data[4]
			orderlist.save()
		bus_join_data_split_return=bus_join_data_return.split('-')
		print "bus_join_data_split", bus_join_data_split_return
		for i in range(0,len(bus_join_data_split_return)):
			print "bus_join_data_split", bus_join_data_split_return[i]
			data = bus_join_data_split_return[i].split('_')
			orderlist=OrderList()
			orderlist.order=order
			orderlist.seatnumber=data[1]
			orderlist.firstname=data[2]
			orderlist.lastname=data[3]
			orderlist.age=data[4]
			orderlist.save()

	
	return response

@csrf_exempt
def confirmbook(request):	
	from hashlib import md5, sha512
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	md5str = "travelibibo" + '|' + request.COOKIES.get('bookid') + '|' + "test123"
	secret = sha512(md5str).hexdigest()
	clientkey='test123'
	bookingid=request.COOKIES.get('bookid')
	print secret
	print clientkey
	print bookingid
	try:
		query,getbookconform=GO.BookConform(secret,bookingid,clientkey)
	except:
		messages.add_message(request, messages.INFO,'Something wrong from API')
		return HttpResponseRedirect(format_redirect_url("bus/bus_booking.html", 'error=6'))
	print getbookconform
	if 'status' in getbookconform:
		log_function(query, "success:"+str(getbookconform['status']))
	else:
		log_function(query, "success:False" + str(getbookconform['Error']))
	response = render_to_response('bus/success-payment.html',{'status':getbookconform},context_instance=RequestContext(request))
	
	#Code for storing PayU Details
	payid, paystatus=store_payudetails(request)
	print "payid", payid
	print "paystatus", paystatus
	response.set_cookie('payudetails',payid)
	response.set_cookie('payustatus',paystatus)
	
	#Code for storing Transaction Details
	transaction = Transaction()
	transaction.order=Order.objects.get(id=request.COOKIES.get('orderdetails'))
	transaction.payu_details=PayuDetails.objects.get(id=payid)
	transaction.payu_status=request.COOKIES.get('payustatus')
	transaction.tentativebooking_id=bookingid
	print transaction.tentativebooking_id
	transaction.tentativebooking_status="processing"
	transaction.save()
	busbookingstatus(request)

	send_templated_mail(
					template_name='payment_bus',
					from_email='testmail123sample@gmail.com',
					recipient_list=[request.COOKIES.get('email')],
					context={
						'user':request.COOKIES.get('fname'),
						'bookingid':transaction.tentativebooking_id,
						'trip':request.COOKIES.get('trip'),
						# 'amount':request.COOKIES.get('guest'),
						'start':request.COOKIES.get('start'),
						'end':request.COOKIES.get('end'),
						'source':request.COOKIES.get('source'),
						'destination':request.COOKIES.get('destination'),
						'totalfare':request.COOKIES.get('total_amount'),
						'totalseats':request.COOKIES.get('totalseats'),
						# 'rooms':request.COOKIES.get('rooms'),
						# 'guest':request.COOKIES.get('guest'),
					},
				)
	return response
	#return HttpResponse(simplejson.dumps(getbookconform['status']), mimetype='application/json')
	
def busbookstatus(request):
	return render_to_response('bus/busbookingstatus.html', context_instance=RequestContext(request)) 

def busbookingstatus(request):
	"""
	Booking Status
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	pid=request.POST.get('bookid')
	try:
		query,getbookingstatus=GO.BookStatus(pid)
		try:
			status={}
			for k,v in getbookingstatus.iteritems():
				for j in v:
					status['status']=j['status']
					status['Destination']=j['Destination']
					status['Travels']=j['Travels']
					status['Source']=j['Source']
					status['TicketStatus']=j['TicketStatus']
					status['BPContactNumber']=j['BPDetails']['BPContactNumber']
					status['BPName']=j['BPDetails']['BPName']
					status['BPLandmark']=j['BPDetails']['BPLandmark']
					status['BPLocation']=j['BPDetails']['BPLocation']
					status['BPAddress']=j['BPDetails']['BPAddress']
			print "getbookingstatus_new", getbookingstatus
		except:
			messages.add_message(request, messages.INFO,'Your booking till queued')
			return HttpResponseRedirect(format_redirect_url("/v2/busbookstatus", 'error=9'))

	except:
		messages.add_message(request, messages.INFO,'Warning message')
		return HttpResponseRedirect(format_redirect_url("/v2/busbookstatus", 'error=7'))
	if 'data' in getbookingstatus:
		log_function(query, "success:True")
	else:
		log_function(query, "success:False" + str(getbookingstatus['Error']))

	#return HttpResponse(simplejson.dumps(status), mimetype='application/json')
	return render_to_response("bus/bookingstatusresult.html",{'status':status}, context_instance=RequestContext(request))

def buscencelticket(request):
	return render_to_response('bus/buscancelticket.html', context_instance=RequestContext(request))

def cancelticket(request):
	"""
	CancelTicket Bus
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	pid=request.POST.get('bookid')
	try:
		query,getcancelticket=GO.CancelTicket(pid)
		if 'data' in getcancelticket:
			log_function(query, "success:True"+str(getcancelticket))
		else:
			log_function(query, "success:False" + str(getcancelticket['Error']))
	except:
		messages.add_message(request, messages.INFO,'Warning message')
		return HttpResponseRedirect(format_redirect_url("/v2/cancelticket", 'error=12'))
	#return HttpResponse(simplejson.dumps(getcancelticket['data']), mimetype='application/json')	
	return render_to_response("bus/conformcancel.html",{'status':getcancelticket},context_instance=RequestContext(request))
@csrf_exempt
def confirm_v2(request):
	from hashlib import md5, sha512
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	md5str = "travelibibo" + '|' + request.COOKIES.get('bookid') + '|' + "test123"
	secret = sha512(md5str).hexdigest()
	clientkey='test123'
	bookingid=request.COOKIES.get('bookid')
	try:
		query,getbookconform=GO.BookConform(secret,bookingid,clientkey)
	except:
		messages.add_message(request, messages.INFO,'Something wrong from API')
		return HttpResponseRedirect(format_redirect_url("bus/bus_booking.html", 'error=6'))
	print getbookconform
	if 'status' in getbookconform:
		log_function(query, "success:"+str(getbookconform['status']))
	else:
		log_function(query, "success:False" + str(getbookconform['Error']))
	response = render_to_response('v2/bus/busconfirmation_v2.html',{'status':getbookconform},context_instance=RequestContext(request))
	
	#Code for storing PayU Details
	payid, paystatus=store_payudetails(request)
	print "payid", payid
	print "paystatus", paystatus
	response.set_cookie('payudetails',payid)
	response.set_cookie('payustatus',paystatus)
	
	#Code for storing Transaction Details
	transaction = Transaction()
	transaction.order=Order.objects.get(id=request.COOKIES.get('orderdetails'))
	transaction.payu_details=PayuDetails.objects.get(id=payid)
	transaction.payu_status=request.COOKIES.get('payustatus')
	transaction.tentativebooking_id=bookingid
	print transaction.tentativebooking_id
	transaction.tentativebooking_status="processing"
	transaction.save()
	busbookingstatus(request)

	send_templated_mail(
					template_name='payment_bus',
					from_email='testmail123sample@gmail.com',
					recipient_list=[request.COOKIES.get('email')],
					context={
						'user':request.COOKIES.get('fname'),
						'bookingid':transaction.tentativebooking_id,
						'trip':request.COOKIES.get('trip'),
						# 'amount':request.COOKIES.get('guest'),
						'start':request.COOKIES.get('start'),
						'end':request.COOKIES.get('end'),
						'source':request.COOKIES.get('source'),
						'destination':request.COOKIES.get('destination'),
						'totalfare':request.COOKIES.get('total_amount'),
						'totalseats':request.COOKIES.get('totalseats'),
						# 'rooms':request.COOKIES.get('rooms'),
						# 'guest':request.COOKIES.get('guest'),
					},
				)
	return response
	#return render_to_response("v2/bus/busconfirmation_v2.html",context_instance=RequestContext(request))

