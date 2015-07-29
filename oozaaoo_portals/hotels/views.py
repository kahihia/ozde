from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from templated_email import send_templated_mail
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from hotels.forms import RegistrationForm


def home(request):
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
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
    return render_to_response('login.html', context_instance=RequestContext(request))
							  