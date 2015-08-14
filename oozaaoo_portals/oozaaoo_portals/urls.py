from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^register', 'hotels.views.registration', name='registration'),
    url(r'^login', 'hotels.views.login_user', name='login_user'),
    url(r'^logout', 'hotels.views.logout_view', name='logout_view'),
    url(r'^myprofile', 'hotels.views.myprofile', name='myprofile'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'', include('social_auth.urls')),
	url(r'^$', 'hotels.views.home', name='home'),
    url(r'^getcity/', 'hotels.views.getcitylist', name='getcitylist'),
    url(r'^gethotellist/', 'hotels.views.gethotellist', name='gethotellist'),
    url(r'^gethoteldetails/', 'hotels.views.gethoteldetails', name='gethoteldetails'),    
    url(r'^setprovisionalbooking/', 'hotels.views.setprovisionalbooking', name='setprovisionalbooking'),
    url(r'^confirmbooking/', 'hotels.views.confirmbooking', name='confirmbooking'),
    url(r'^getbookstatus/', 'hotels.views.getbookingstatus', name='getbookingstatus'),
    url(r'^bookingstatus/', 'hotels.views.bookingstatus', name='bookingstatus'),
    url(r'^cancelbooking/', 'hotels.views.bookingstatus', name='bookingstatus'),
    url(r'^loadcitylist/', 'hotels.views.loadcitylist', name='loadcitylist'),
    url(r'^getrefund/', 'hotels.views.getrefund', name='getrefund'),
    url(r'^confirmcancel/', 'hotels.views.confirmcancel', name='confirmcancel'),

    url(r'^payment/', 'payu.views.buy_order', name='payment'),
    url(r'^bookhotel/', 'hotels.views.userdetails', name='userdetails'),
        
    #=============================BUS URL=========================#
    url(r'^searchbus/', 'bus.views.search_bus', name='search_bus'),
    url(r'^seat_map/', 'bus.views.seat_map', name='seat_map'),
    url(r'^bus_booking/','bus.views.bus_booking', name='bus_booking'),
    url(r'^cancelpolicy/', 'bus.views.cancelpolicy', name='cancelpolicy'),
    url(r'^cancelticket/', 'bus.views.cancelticket', name='cancelticket'),
    url(r'^buscancelticket/', 'bus.views.buscencelticket', name='buscencelticket'),
    url(r'^bus_payu/', 'payu.views.bus_payu', name='bus_payu'),
    url(r'^confirmbook/', 'bus.views.confirmbook', name='confirmbook'),
    url(r'^busbookstatus/', 'bus.views.busbookstatus', name='busbookstatus'),
    url(r'^busbookingstatus/', 'bus.views.busbookingstatus', name='busbookingstatus'),
    url(r'^tentativebooking/', 'bus.views.tentativebooking', name='tentativebooking'),
    #============================forgetpassword========================#
    url(r'^(?i)password_reset/$', 'django.contrib.auth.views.password_reset', {
      'template_name':'registration/password_reset_form.html',
      'email_template_name':'registration/password_reset_email.html'
    }, name="password_reset"),
    url(r'^(?i)user/password/reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/user/password/reset/done/'}),
    url(r'^(?i)user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^(?i)user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/user/password/done/'}),
    url(r'^(?i)user/password/done/$', 
        'django.contrib.auth.views.password_reset_complete'),	
)
