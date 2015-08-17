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

class mydict(dict):
        def __str__(self):
            return json.dumps(self)

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
		getbusresponse=GO.Searchbus(source, destination, dateofdeparture, dateofarrival)
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
					# joindata_bus = unicode(dateofdeparture)+"-"+unicode(bussearchlist['TravelsName'])+"-"+unicode(bussearchlist['fare'])+"-"+unicode(source)+"_"+unicode(destination)
										
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
			messages.add_message(request, messages.INFO,'API not responding for one way tripa')
			return HttpResponseRedirect(format_redirect_url("/", 'error=2'))
	except:
		messages.add_message(request, messages.INFO,'User Entering data is wrong')
		return HttpResponseRedirect(format_redirect_url("/", 'error=1'))

	source = unicode(source)
	destination = unicode(destination)
	# joindata_bus = dateofdeparture+"-"+TravelsName+"-"+fare+"-"+source+"-"+destination
	#return HttpResponse(simplejson.dumps(reviews), mimetype='application/json')
	if trip=='oneway':	
		response = render_to_response('bus/bus-searchlist.html', {'reviews':reviews}, context_instance=RequestContext(request))
	else:
		response = render_to_response('bus/bus-searchlist-round.html', {'reviews':reviews,'reviews_return':reviews_return}, context_instance=RequestContext(request))

	response.set_cookie( 'source', source)
	response.set_cookie( 'trip', trip)
	response.set_cookie( 'destination', destination)
	response.set_cookie( 'start', departure)
	return response

@csrf_exempt	
def seat_map(request):
	"""
	Seat Map Info 
	"""
	skey=request.POST.get('skey',request.COOKIES.get('skey')) 
	try:
		GO = goibiboAPI('apitesting@goibibo.com', 'test123')
		getbusseat=GO.Busseat(skey)
		results=[]
		for k,v in getbusseat.iteritems():
			results.append(v['onwardSeats'])
			for s,i in v['onwardBPs']['GetBoardingPointsResult'].iteritems():
				results.append(i)
	except:
		messages.add_message(request, messages.INFO,'Search key not given by API.skey is %s'%request.POST.get('skey',request.COOKIES.get('skey')))
		return HttpResponseRedirect(format_redirect_url("/", 'error=4'))
	#return HttpResponse(simplejson.dumps(results), mimetype='application/json')
	#return simplejson.dumps(results)
	response= render_to_response('bus/bus-seatmapinfo.html', {'results':results}, context_instance=RequestContext(request)) 
	response.set_cookie('skey',skey)
	return response

def cancelpolicy(request):
	"""
	CancelPolicy for the Particular Bus
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	skey='x55sNj4nk-c4y5eIGdK6Kv4V8NAKn5hNfNwfAeSDMq1E-i00KtoMqjSfVHVRB-I='
	getcencelpolicy=GO.CancelPolicy(skey)
	policy=[]
	for k,v in getcencelpolicy.iteritems():
		 for key in v.iteritems():
			policy.append(key)

	# return HttpResponse(simplejson.dumps(policy), mimetype='application/json')
	return render_to_response('bus/bus-cancelpolicy.html', {'policy':policy}, context_instance=RequestContext(request)) 

@login_required(login_url='/register/')
def bus_booking(request):
	
	try:
		bpoint=request.POST.get('bpoint',request.COOKIES.get('bpoint'))
		bpoint_id,bpoint_name= bpoint.split("-")
		seatdetails=request.POST.get('seat',request.COOKIES.get('seatdetails'))
		fare , seat_name=seatdetails.split(",")
		response= render_to_response('bus/bus_booking.html', context_instance=RequestContext(request)) 
		response.set_cookie('bpoint',bpoint)
		response.set_cookie('seatdetails',seatdetails)
		response.set_cookie('bpoint_id',bpoint_id)
		response.set_cookie('bpoint_name',bpoint_name)
		response.set_cookie('seat_fare',fare)
		response.set_cookie('seat_name',seat_name)
		return response
	except:
		messages.add_message(request, messages.INFO,'Enter the details correct way')
		trip = request.COOKIES.get('trip')
		if trip=='oneway':	
			return HttpResponseRedirect(format_redirect_url("/searchbus", 'error=8'))
		else:
			return HttpResponseRedirect(format_redirect_url("/searchbus", 'error=8'))


def tentativebooking(request):
	print "tentativebooking"
	import requests
	import urllib
	from django.utils import simplejson
	skey=request.POST.get('skey',request.COOKIES.get('skey'))
	bpoint_id=request.COOKIES.get('bpoint_id')
	bpoint_name=request.COOKIES.get('bpoint_name')
	seat_fare=request.COOKIES.get('seat_fare')
	seat_name=request.COOKIES.get('seat_name')
	title=request.POST.get('title',request.COOKIES.get('title'))
	fname=request.POST.get('fname',request.COOKIES.get('fname'))
	lname=request.POST.get('lname',request.COOKIES.get('lname'))
	age=request.POST.get('age',request.COOKIES.get('age'))
	email=request.POST.get('email',request.COOKIES.get('email'))
	mobile=request.POST.get('mobile',request.COOKIES.get('mobile'))
	bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age
	url = "http://pp.goibibobusiness.com/api/bus/hold/"
	customer = [['title', 'Mr'],
			   ['firstName', fname], 
               ['lastName',lname], 
               ['age',age], 
               ['eMail',email], 
               ['mobile',mobile],
               ['seatName', seat_name],
               ['seatFare',seat_fare],
               ]
	customer_details=[mydict(customer)]
	bus=[['skey',request.COOKIES.get('skey')],
		['bp',request.COOKIES.get('bpoint_id')],
		['seats',customer_details]]
	bus_info=mydict(bus)
	onw=[['onw',bus_info]]
	onw_info=mydict(onw)
	payload={'holddata':'%s'%onw_info}
	#payload={'holddata':'{"onw":{"skey":"zJ5yLDs6ptU20KB7EtLDKv4V6NMMmZNKNqDi0J5O-msWyzc9Eww-7nLdgbubveJxLR_t0-R8Lg==","bp":"66677","seats":[{"title":"Mr","firstName":"test","lastName":"test","age":"34","eMail":"goibibobusinesstest@gmail.com","mobile":"9888888888","seatName":"36","seatFare":"122"}]}}'}
	headers = {
        'content-type': "application/x-www-form-urlencoded"
    }
	details = requests.request("POST", url, data=payload, headers=headers, auth=('apitesting@goibibo.com','test123'))
	#response=HttpResponse(details)
	# return HttpResponse(simplejson.dumps(response), mimetype='application/json')
	try:
		from datetime import datetime
		fmt = '%Y/%m/%d'
		order=Order()	
		order.userprofile =UserProfile.objects.get(user=request.user)
		order.trip=request.COOKIES.get('trip')
		order.source=request.COOKIES.get('source')
		order.destination=request.COOKIES.get('destination')
		order.start_date=datetime.strptime(request.COOKIES.get('start'), fmt)
		order.end_date=datetime.strptime(request.COOKIES.get('end'), fmt)
		order.totalseats=request.COOKIES.get('totalseats')
		order.boardingpoint_id=request.COOKIES.get('bpoint_id')
		order.boardingpoint_name=request.COOKIES.get('bpoint_name')
		order.amount=request.COOKIES.get('prc')
		order.category_type="bus"
		order.save()
		response.set_cookie('orderdetails',order.id)
		response.set_cookie('category_type',order.category_type)
		store_payudetails()
		response=HttpResponseRedirect("/bus_payu/")#,{'response':response,'joindata_bus':joindata_bus}
	except:
		messages.add_message(request, messages.INFO,'Enter the details correct way')
		return HttpResponseRedirect(format_redirect_url("bus/bus_booking.html", 'error=5'))
	print details.json()
	response.set_cookie('bookid',details.json()['data']['bookingID'])
	response.set_cookie('fname',fname)
	response.set_cookie('lname',lname)
	response.set_cookie('age',age)
	response.set_cookie('email',email)
	response.set_cookie('mobile',mobile)
	response.set_cookie('bus_join_data',bus_join_data)	
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
		getbookconform=GO.BookConform(secret,bookingid,clientkey)
	except:
		messages.add_message(request, messages.INFO,'Something wrong from API')
		return HttpResponseRedirect(format_redirect_url("bus/bus_booking.html", 'error=6'))
	print getbookconform

	transaction = Transaction()
	transaction.order=Order.objects.get(id=request.COOKIES.get('orderdetails'))
	transaction.payu_details=PayuDetails.objects.get(id=request.COOKIES.get('payudetails'))
	transaction.tentativebooking_id=bookingid
	transaction.tentativebooking_status="processing"
	transaction.save
	busbookingstatus(request)
	return render_to_response('bus/success-payment.html',{'status':getbookconform},context_instance=RequestContext(request))
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
		getbookingstatus=GO.BookStatus(pid)
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
		messages.add_message(request, messages.INFO,'Booking id not given by API')
		return HttpResponseRedirect(format_redirect_url("busbookstatus", 'error=7'))

	return HttpResponse(simplejson.dumps(status), mimetype='application/json')

def buscencelticket(request):
	return render_to_response('bus/buscancelticket.html', context_instance=RequestContext(request))

def cancelticket(request):
	"""
	CancelTicket Bus
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	pid=request.POST.get('bookid')
	getcancelticket=GO.CancelTicket(pid)
	return HttpResponse(simplejson.dumps(getcancelticket['data']), mimetype='application/json')	

