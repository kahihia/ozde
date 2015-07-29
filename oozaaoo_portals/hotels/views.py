from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404

def home(request):
	return render_to_response('login-register.html')