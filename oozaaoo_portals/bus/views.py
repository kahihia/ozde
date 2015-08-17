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

def search_bus(request):
	"""
	Search Bus based on Source and Destination
	"""
	try:
		GO = goibiboAPI('apitesting@goibibo.com', 'test123')
		source= request.POST.get('source',request.COOKIES.get('source'))
		destination=request.POST.get('destination',request.COOKIES.get('destination'))
		departure=request.POST.get('start',request.COOKIES.get('start'))
		dateofdeparture = departure.replace('/','')
		arrival=request.POST.get('end',request.COOKIES.get('end'))
		dateofarrival = departure.replace('/','')
		trip=request.POST.get('trip',request.COOKIES.get('trip'))		
	except:
		print'source', source
		print'destination',destination
		print'dateofarrival',dateofarrival
		print'dateofdeparture',dateofdeparture
		print'trip',trip
		messages.add_message(request, messages.INFO,'you cannot directly move page')
		return HttpResponseRedirect(format_redirect_url("/", 'error=10'))
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
		print getbusresponse
		messages.add_message(request, messages.INFO,'User Entering data is wrong')
		return HttpResponseRedirect(format_redirect_url("/", 'error=1'))

	source = unicode(source)
	destination = unicode(destination)
	# joindata_bus = dateofdeparture+"-"+TravelsName+"-"+fare+"-"+source+"-"+destination
	#return HttpResponse(simplejson.dumps(reviews), mimetype='application/json')
	if trip=='oneway':	
		response = render_to_response('bus/bus-searchlist.html', {'reviews':reviews,'source':source,'destination':destination}, context_instance=RequestContext(request))
	else:
		response = render_to_response('bus/bus-searchlist-round.html', {'reviews':reviews,'reviews_return':reviews_return,'source':source,'destination':destination}, context_instance=RequestContext(request))

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
		totalfare=request.POST.get('total_seat_amount')
		print totalfare
		selected_seats=request.POST.getlist('available_seat')
		print'selected_seats', selected_seats
		selected_seats_fare=request.POST.getlist('available_seat_fare')
		print'selected_seats_fare', selected_seats_fare
		bpoint=request.POST.get('bpoint',request.COOKIES.get('bpoint'))
		print bpoint
		bpoint_id,bpoint_name= bpoint.split("-")
		print bpoint_id
		# seatdetails=request.POST.get('seat',request.COOKIES.get('seatdetails'))
		# fare , seat_name=seatdetails.split(",")
		response= render_to_response('bus/bus_booking.html',{'total_amt':totalfare,'seat':selected_seats,'fare':selected_seats_fare}, context_instance=RequestContext(request)) 
		response.set_cookie('bpoint',bpoint)
		#response.set_cookie('seatdetails',seatdetails)
		response.set_cookie('bpoint_id',bpoint_id)
		response.set_cookie('bpoint_name',bpoint_name)
		response.set_cookie('totalfare',totalfare)
		response.set_cookie('selected_seats',selected_seats)
		response.set_cookie('total_seats',len(selected_seats))
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
	seat_fare=int(totalfare)/int(total_seat)
	title=request.POST.get('title_1',request.COOKIES.get('title'))
	fname=request.POST.get('fname_1',request.COOKIES.get('fname'))
	lname=request.POST.get('lname_1',request.COOKIES.get('lname'))
	seat_name=request.POST.get('seat_1',request.COOKIES.get('seat'))
	age=request.POST.get('age_1',request.COOKIES.get('age'))
	title1=request.POST.get('title_2')
	fname1=request.POST.get('fname_2')
	lname1=request.POST.get('lname_2')
	seat_name1=request.POST.get('seat_2')
	age1=request.POST.get('age_2')
	title2=request.POST.get('title_3')
	fname2=request.POST.get('fname_3')
	lname2=request.POST.get('lname_3')
	seat_name2=request.POST.get('seat_3')
	age2=request.POST.get('age_3')
	title3=request.POST.get('title_4')
	fname3=request.POST.get('fname_4')
	lname3=request.POST.get('lname_4')
	seat_name3=request.POST.get('seat_4')
	age3=request.POST.get('age_4')
	title4=request.POST.get('title_5')
	fname4=request.POST.get('fname_5')
	lname4=request.POST.get('lname_5')
	seat_name4=request.POST.get('seat_5')
	age4=request.POST.get('age_5')
	title5=request.POST.get('title_6')
	fname5=request.POST.get('fname_6')
	lname5=request.POST.get('lname_6')
	seat_name5=request.POST.get('seat_6')
	age5=request.POST.get('age_6')
	email=request.POST.get('email',request.COOKIES.get('email'))
	mobile=request.POST.get('mobile',request.COOKIES.get('mobile'))
	if total_seat == '6':
		bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_name3+"_"+fname3+"_"+lname3+"_"+age3+"-5_"+seat_name4+"_"+fname4+"_"+lname4+"_"+age4+"-6_"+seat_name5+"_"+fname5+"_"+lname5+"_"+age5
	elif total_seat == '5':
		bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_name3+"_"+fname3+"_"+lname3+"_"+age3+"-5_"+seat_name4+"_"+fname4+"_"+lname4+"_"+age4
	elif total_seat == '4':
		bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_name2+"_"+fname2+"_"+lname2+"_"+age2+"-4_"+seat_name3+"_"+fname3+"_"+lname3+"_"+age3
	elif total_seat == '3':
		bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_name1+"_"+fname1+"_"+lname1+"_"+age1+"-3_"+seat_name2+"_"+fname2+"_"+lname2+"_"+age2
	elif total_seat == '2':
		bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age+"-2_"+seat_name1+"_"+fname1+"_"+lname1+"_"+age1
	else:
		bus_join_data="1_"+seat_name+"_"+fname+"_"+lname+"_"+age

	print bus_join_data
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
	#try:
	response.set_cookie('bookid',details.json()['data']['bookingID'])
	# except:
	# 	temp= details.json()
	# 	if temp.has_key("data"):
	# 		messages.add_message(request, messages.INFO,temp['data']['error']+'.Please Search again')
	# 	else:
	# 		messages.add_message(request, messages.INFO,temp['Error']+'.Please Search again')
	# 	return HttpResponseRedirect(format_redirect_url("/bus_booking", 'error=11'))
	response.set_cookie('fname',fname)
	response.set_cookie('lname',lname)
	response.set_cookie('age',age)
	response.set_cookie('email',email)
	response.set_cookie('mobile',mobile)
	response.set_cookie('bus_join_data',bus_join_data)
	seat_name
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
		print 'getbookingstatus',getbookingstatus
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
		except:
			messages.add_message(request, messages.INFO,'Your booking till queued')
			return HttpResponseRedirect(format_redirect_url("/busbookstatus", 'error=9'))

	except:
		messages.add_message(request, messages.INFO,'Booking id not given by API')
		return HttpResponseRedirect(format_redirect_url("/busbookstatus", 'error=7'))

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

