from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^register', 'hotels.views.registration', name='registration'),
    url(r'^v2/register', 'hotels.views.registration_v2', name='registration_v2'),
    url(r'^login', 'hotels.views.login_user', name='login_user'),
    url(r'^v2/login', 'hotels.views.login_user_v2', name='login_user_v2'),
    url(r'^logout', 'hotels.views.logout_view', name='logout_view'),
    url(r'^v2/logout', 'hotels.views.logout_view_v2', name='logout_view_v2'),
    url(r'^v2/test', 'hotels.views.test_view_v2', name='test_view_v2'),
    url(r'^myprofile', 'hotels.views.myprofile', name='myprofile'),
     url(r'^mybooking', 'hotels.views.mybooking', name='mybooking'),
    url(r'^admin/', include(admin.site.urls)),
	# url(r'', include('social_auth.urls')),
	url(r'^$', 'hotels.views.home_v2', name='home_v2'),
    url(r'^profile_details/$', 'hotels.views.profile_details', name='profile_details'),
    url(r'^settings/$', 'hotels.views.settings', name='settings'),

    # url(r'^v2/$', 'hotels.views.home_v2', name='home_v2'),
    url(r'^v2/profile$', 'hotels.views.profile_v2', name='profile_v2'),
    url(r'^getcity/', 'hotels.views.getcitylist', name='getcitylist'),
    url(r'^gethotellist/', 'hotels.views.gethotellist', name='gethotellist'),
    url(r'^v2/gethotellist/', 'hotels.views.gethotellist_v2', name='gethotellist_v2'),
    url(r'^gethoteldetails/', 'hotels.views.gethoteldetails', name='gethoteldetails'),
    url(r'^v2/gethoteldetails/', 'hotels.views.gethoteldetails_v2', name='gethoteldetails_v2'),
    url(r'^setprovisionalbooking/', 'hotels.views.setprovisionalbooking', name='setprovisionalbooking'),
    url(r'^v2/setprovisionalbooking/', 'hotels.views.setprovisionalbooking_v2', name='setprovisionalbooking_v2'),
    url(r'^v2/confirmbooking/', 'hotels.views.confirmbooking_v2', name='confirmbooking_v2'),
    #url(r'^confirmbooking/(?P<pid>.*)/(?P<udf1>.*)/(?P<pinfo>.*)/(?P<email>.*)/$', 'hotels.views.confirmbooking', name='confirmbooking'),
    url(r'^getbookstatus/', 'hotels.views.getbookingstatus', name='getbookingstatus'),
    url(r'^bookingstatus/', 'hotels.views.bookingstatus', name='bookingstatus'),
    url(r'^v2/bookingstatus/', 'hotels.views.bookingstatus_v2', name='bookingstatus_v2'),
    url(r'^getbookdetails/', 'hotels.views.getbookingdetails', name='getbookingdetails'),
    url(r'^loadcitylist/', 'hotels.views.loadcitylist', name='loadcitylist'),
    url(r'^refund/', 'hotels.views.refund', name='refund'),
    url(r'^getrefund/', 'hotels.views.getrefund', name='getrefund'),
    url(r'^confirmcancel/', 'hotels.views.confirmcancel', name='confirmcancel'),
    url(r'^bookinginfo/', 'hotels.views.bookinginfo', name='bookinginfo'),
    url(r'^cancelhotel/', 'hotels.views.cancelhotel', name='cancelhotel'),
    url(r'^payment/', 'payu.views.buy_order', name='payment'),
    url(r'^v2/bookhotel/', 'hotels.views.userdetails_v2', name='userdetails_v2'),
    url(r'^bookhotel/', 'hotels.views.userdetails', name='userdetails'),
    url(r'^get_results_by_price/', 'hotels.views.get_results_by_price', name='get_results_by_price'),

    #=============================BUS URL=========================#
    url(r'^searchbus/', 'bus.views.search_bus', name='search_bus'),
    url(r'^v2/searchbus/', 'bus.views.search_bus_v2', name='search_bus_v2'),
    url(r'^seat/', 'bus.views.seat', name='seat'),
    url(r'^seat_v2/', 'bus.views.seat_v2', name='seat_v2'),
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
    url(r'^v2/tentativebooking/', 'bus.views.tentativebooking_v2', name='tentativebooking_v2'),
    url(r'^v2/confirm/', 'bus.views.confirm_v2', name='confirm_v2'),
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
    #==============================other links============================#
    url(r'^v2/terms_and_condition/', 'hotels.views.terms_and_condition', name='terms_and_condition'),
    url(r'^aboutus/', 'hotels.views.aboutus', name='aboutus'),
    url(r'^v2/privacy/', 'hotels.views.privacy', name='privacy'),
    url(r'^contactus/', 'hotels.views.contactus', name='contactus'),


	#==============================Flight_search==========================#
	url(r'^iata_code/', 'flight.views.iata_code', name='iata_code'),
	url(r'^SearchFlight/', 'flight.views.search_flights', name='search_flights'),
	url(r'^FlightBooking/', 'flight.views.flight_details', name='flight_details'),
	url(r'^TentativeBooking/', 'flight.views.tentativebooking', name='tentativebooking'),
	url(r'^FlightConfirm/', 'flight.views.flight_confirm', name='flight_confirm'),

)
