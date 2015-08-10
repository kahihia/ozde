import requests
import logging
import random
import string
import json

from django.utils import simplejson
from json import dumps, loads
import simplejson as json

from apiservice.views import *

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


def search_bus(request):
	"""
	Search Bus based on Source and Destination
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	source='chennai'
	destination='banglore'
	dateofdeparture=20150812
	dateofarrival=''
	getbusresponse=GO.Searchbus(source, destination, dateofdeparture, dateofarrival)
	reviews = []
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
				print'==============>', len(morevalues)
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

	joindata_bus = unicode(dateofdeparture)
	travel_name = unicode(bussearchlist['TravelsName'])
	fare = unicode(bussearchlist['fare']['totalfare'])
	source = unicode(source)
	destination = unicode(destination)
	# joindata_bus = dateofdeparture+"-"+TravelsName+"-"+fare+"-"+source+"-"+destination
	# return HttpResponse(simplejson.dumps(reviews), mimetype='application/json')	
	response = render_to_response('bus/bus-searchlist.html', {'reviews':reviews}, context_instance=RequestContext(request))
	response.set_cookie( 'joindata_bus', joindata_bus)
	response.set_cookie( 'travel_name', travel_name)
	response.set_cookie( 'fare', fare)
	response.set_cookie( 'source', source)
	response.set_cookie( 'destination', destination)
	return response
	
def seat_map(request):
	"""
	Seat Map Info 
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	skey='xJ51Ly0ti91R1ZOEFuDFKv4V6dUJm5pKNqDh0J5O9mobyjc9Eww-7nLdgbubveJxLR_t0-N8Lg=='
	getbusseat=GO.Busseat(skey)
	results=[]
	for k in getbusseat['data']['onwardSeats']:
		results.append(k)
	# return HttpResponse(simplejson.dumps(results), mimetype='application/json')
	return render_to_response('bus/bus-seatmapinfo.html', {'results':results}, context_instance=RequestContext(request)) 


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

def tentativebooking(request):
	import requests
	import urllib
	from django.utils import simplejson
	url = "http://pp.goibibobusiness.com/api/bus/hold/"
	joindata_bus= request.COOKIES.get('joindata_bus')	
	payload={'holddata':'{"onw":{"skey":"zJ5yLDs6ptU20KB7EtLDKv4V6NMMmZNKNqDi0J5O-msWyzc9Eww-7nLdgbubveJxLR_t0-R8Lg==","bp":"66677","seats":[{"title":"Mr","firstName":"test","lastName":"test","age":"34","eMail":"goibibobusinesstest@gmail.com","mobile":"9888888888","seatName":"36","seatFare":"122"}]}}'}
	headers = {
        'content-type': "application/x-www-form-urlencoded"
    }
	response = requests.request("POST", url, data=payload, headers=headers, auth=('apitesting@goibibo.com','test123'))
	# return HttpResponse(response)
	# return HttpResponse(simplejson.dumps(response), mimetype='application/json')
	return render_to_response('bus/bus-tentativebooking.html',{'response':response,'joindata_bus':joindata_bus},context_instance=RequestContext(request))


def confirmbooking(request):	
	"""
	CancelTicket Bus
	"""
	from hashlib import md5, sha512
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	md5str = "travelibibo" + '|' + "GOBUS0d1441438774394" + '|' + "test123"
	secret = sha512(md5str).hexdigest()
	clientkey='test123'
	bookingid='GOBUS0d1441438774394'
	getbookconform=GO.BookConform(secret,bookingid,clientkey)
	busdetails=request.COOKIES.get('reviews')
	print(busdetails)
	return render_to_response('bus/bus-confirmbook.html',{'status':status},context_instance=RequestContext(request))
	# return HttpResponse(simplejson.dumps(getbookconform['status']), mimetype='application/json')
	
def bookingstatus(request):
	"""
	Booking Status
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	pid='GOBUS0d1441438774394'
	getbookingstatus=GO.BookStatus(pid)
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
	return HttpResponse(simplejson.dumps(status), mimetype='application/json')

def cancelticket(request):
	"""
	CancelTicket Bus
	"""
	GO = goibiboAPI('apitesting@goibibo.com', 'test123')
	pid='GOBUS0693d143'
	getcancelticket=GO.CancelTicket(pid)
	return HttpResponse(simplejson.dumps(getcancelticket['data']), mimetype='application/json')	

