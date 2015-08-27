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
			return HttpResponseRedirect(format_redirect_url("/", 'error=2'))
	except:
		messages.add_message(request, messages.INFO,'User Entering data is wrong')
		return HttpResponseRedirect(format_redirect_url("/", 'error=1'))

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

def search_bus_v2(request):
	"""
	Search Bus based on Source and Destination
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	source= request.POST.get('source',request.COOKIES.get('source'))
	destination=request.POST.get('destination',request.COOKIES.get('destination'))
	departure=request.POST.get('start',request.COOKIES.get('start'))
	month,date,year=departure.split('/')
	dateofdeparture = year+month+date
	print dateofdeparture
	arrival=request.POST.get('end',request.COOKIES.get('end'))
	month,date,year=arrival.split('/')
	dateofarrival = year+month+date
	print dateofarrival
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
			return HttpResponseRedirect(format_redirect_url("/", 'error=2'))
	except:
		messages.add_message(request, messages.INFO,'User Entering data is wrong')
		return HttpResponseRedirect(format_redirect_url("/", 'error=1'))

	source = unicode(source)
	destination = unicode(destination)
	# joindata_bus = dateofdeparture+"-"+TravelsName+"-"+fare+"-"+source+"-"+destination
	#return HttpResponse(simplejson.dumps(reviews), mimetype='application/json')
	if trip=='oneway':	
		#response = render_to_response('bus/bus-searchlist.html', {'reviews':reviews}, context_instance=RequestContext(request))
		response = HttpResponse(simplejson.dumps(reviews), mimetype='application/json')

	else:
		#response = render_to_response('bus/bus-searchlist-round.html', {'reviews':reviews,'reviews_return':reviews_return}, context_instance=RequestContext(request))
		response = HttpResponse(simplejson.dumps(reviews_return), mimetype='application/json')

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
		return HttpResponseRedirect(format_redirect_url("/", 'error=4'))
	response = HttpResponse(simplejson.dumps(getbusseat), mimetype='application/json')
	#response= simplejson.dumps(results)
	# response= render_to_response('bus/bus-seatmapinfo.html', {'results':results}, context_instance=RequestContext(request)) 
	response.set_cookie('skey',skey)
	return response

@csrf_exempt
def seat(request):
	skey=request.POST.get('skey',request.COOKIES.get('skey'))
	bus_type=request.POST.get('bus_type',request.COOKIES.get('bus_type'))

	seat_type=bus_type.lower().split()
	number= seat_type[-1]
	name= seat_type[:-1]
	trip=request.COOKIES.get('trip')
	print 'trip====',trip
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
		response= render_to_response('bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'seater' in name and number=='(2+2)':
		response= render_to_response('bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'airbus' in name and number=='(2+2)':
		response= render_to_response('bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'semisleeper' in name and number=='(2+2)':
		response= render_to_response('bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'sleeper' in name and number=='(2+1)':
		response= render_to_response('bus/sleeper(2+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'sleeper' in name and number=='(1+1)':
		response= render_to_response('bus/sleeper(1+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	elif 'seater/sleeper' in name and number=='(2+1)' or 'seater' in name and'sleeper' in name and number=='(2+1)':
		response= render_to_response('bus/seater_sleeper(2+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request))
	elif 'seater' in name or 'sleeper' in name and number=='(1+1+1)':
		response= render_to_response('bus/seater(1+1+1).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request))
	elif 'seater' in name and number=='(2+3)':
		response= render_to_response('bus/seater(2+3).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request))
	else:
		response= render_to_response('bus/seater(2+2).html', {'skey':skey,'result':results,'trip':trip}, context_instance=RequestContext(request)) 
	
	response.set_cookie('skey',skey)
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


@login_required(login_url='/register/')
def bus_booking(request):	
	try:
		totalfare=request.POST.get('totalfare')
		print totalfare
		count_of_seat=request.POST.get('seatcount')
		print'count_of_seat', count_of_seat
		selected_seats_fare=request.POST.get('seatFare')
		selected_seats_fare_split=selected_seats_fare.split(",")
		print'selected_seats_fare', selected_seats_fare_split
		selected_seats=request.POST.get('seatNumbersList')
		selected_seats_split=selected_seats.split(",")
		print 'selected_seats',selected_seats_split
		bpoint=request.POST.get('boarding_point_list',request.COOKIES.get('boarding_point_list'))
		print bpoint
		bpoint_id,bpoint_name= bpoint.split("-")
		print bpoint_id
		seat_and_fare=zip(selected_seats_split,selected_seats_fare_split)
		# seatdetails=request.POST.get('seat',request.COOKIES.get('seatdetails'))
		# fare , seat_name=seatdetails.split(",")
		response= render_to_response('bus/bus_booking.html',{'total_amt':totalfare,'seat':seat_and_fare,'count':count_of_seat}, context_instance=RequestContext(request)) 
		response.set_cookie('bpoint',bpoint)
		#response.set_cookie('seatdetails',seatdetails)
		response.set_cookie('bpoint_id',bpoint_id)
		response.set_cookie('bpoint_name',bpoint_name)
		response.set_cookie('totalfare',totalfare)
		response.set_cookie('selected_seats',selected_seats)
		response.set_cookie('total_seats',count_of_seat)
		return response
	except:
		messages.add_message(request, messages.INFO,'Enter the details correct way')
		trip = request.COOKIES.get('trip')
		if trip=='oneway':	
			return HttpResponseRedirect(format_redirect_url("/searchbus", 'error=8'))
		else:
			return HttpResponseRedirect(format_redirect_url("/searchbus", 'error=8'))


def tentativebooking(request):
	import requests
	import urllib
	from django.utils import simplejson
	skey=request.POST.get('skey',request.COOKIES.get('skey'))
	print 'skey',skey
	bpoint_id=request.COOKIES.get('bpoint_id')
	print 'bpoint_id',bpoint_id
	bpoint_name=request.COOKIES.get('bpoint_name')
	print 'bpoint_name',bpoint_name
	totalfare=request.COOKIES.get('totalfare')
	print 'totalfare',totalfare

	selected_seats=request.COOKIES.get('selected_seat')
	print 'selected_seats',selected_seats

	total_seat=request.COOKIES.get('total_seats')
	print 'total_seat',total_seat
	title=request.POST.get('title_1',request.COOKIES.get('title'))
	print 'title', title
	fname=request.POST.get('fname_1',request.COOKIES.get('fname'))
	lname=request.POST.get('lname_1',request.COOKIES.get('lname'))
	seat_name=request.POST.get('seat_1',request.COOKIES.get('seat'))
	seat_fare=request.POST.get('fare_1',request.COOKIES.get('fare'))
	age=request.POST.get('age_1',request.COOKIES.get('age'))
	title1=request.POST.get('title_2')
	print 'title1', title1
	fname1=request.POST.get('fname_2')
	lname1=request.POST.get('lname_2')
	seat_name1=request.POST.get('seat_2')
	seat_fare1=request.POST.get('fare_2')
	age1=request.POST.get('age_2')
	title2=request.POST.get('title_3')
	print 'title2', title2
	fname2=request.POST.get('fname_3')
	lname2=request.POST.get('lname_3')
	seat_name2=request.POST.get('seat_3')
	seat_fare2=request.POST.get('fare_3')
	age2=request.POST.get('age_3')
	title3=request.POST.get('title_4')
	fname3=request.POST.get('fname_4')
	lname3=request.POST.get('lname_4')
	seat_name3=request.POST.get('seat_4')
	seat_fare3=request.POST.get('fare_4')
	age3=request.POST.get('age_4')
	title4=request.POST.get('title_5')
	fname4=request.POST.get('fname_5')
	lname4=request.POST.get('lname_5')
	seat_name4=request.POST.get('seat_5')
	seat_fare4=request.POST.get('fare_5')
	age4=request.POST.get('age_5')
	title5=request.POST.get('title_6')
	fname5=request.POST.get('fname_6')
	lname5=request.POST.get('lname_6')
	seat_name5=request.POST.get('seat_6')
	seat_fare5=request.POST.get('fare_6')
	age5=request.POST.get('age_6')
	email=request.POST.get('email',request.COOKIES.get('email'))
	mobile=request.POST.get('mobile',request.COOKIES.get('mobile'))
	url = "http://pp.goibibobusiness.com/api/bus/hold/"
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
		return HttpResponseRedirect(format_redirect_url("/bus_booking", 'error=11'))
	response.set_cookie('fname',fname)
	response.set_cookie('lname',lname)
	response.set_cookie('age',age)
	response.set_cookie('email',email)
	response.set_cookie('mobile',mobile)
	response.set_cookie('bus_join_data',bus_join_data)

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
	
	return response

@csrf_exempt
def confirmbook(request):	
	"""
	CancelTicket Bus 
	"""
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
						'totalfare':request.COOKIES.get('totalfare'),
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
			return HttpResponseRedirect(format_redirect_url("/busbookstatus", 'error=9'))

	except:
		messages.add_message(request, messages.INFO,'Warning message')
		return HttpResponseRedirect(format_redirect_url("/busbookstatus", 'error=7'))
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
		return HttpResponseRedirect(format_redirect_url("/cancelticket", 'error=12'))
	#return HttpResponse(simplejson.dumps(getcancelticket['data']), mimetype='application/json')	
	return render_to_response("bus/conformcancel.html",{'status':getcancelticket},context_instance=RequestContext(request))

