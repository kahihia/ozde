from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^register', 'hotels.views.registration', name='registration'),
    url(r'^admin/', include(admin.site.urls)),
	# url(r'', include('social_auth.urls')),
	url(r'^$', 'hotels.views.home', name='home'),
    url(r'^getcity/', 'hotels.views.getcitylist', name='getcitylist'),
    url(r'^gethotellist/', 'hotels.views.gethotellist', name='gethotellist'),
    url(r'^gethoteldetails/', 'hotels.views.gethoteldetails', name='gethoteldetails'),    
    # url(r'^bookhotel/', 'hotels.views.setprovisionalbooking', name='bookhotel'),
    url(r'^confirmbooking/', 'hotels.views.confirmbooking', name='confirmbooking'),
    url(r'^getbookstatus/', 'hotels.views.getbookingstatus', name='getbookingstatus'),
    url(r'^getbookdetails/', 'hotels.views.getbookingdetails', name='getbookingdetails'),
    url(r'^loadcitylist/', 'hotels.views.loadcitylist', name='loadcitylist'),
    url(r'^getrefund/', 'hotels.views.getrefund', name='getrefund'),
    url(r'^confirmcancel/', 'hotels.views.confirmcancel', name='confirmcancel'),

    url(r'^payment/', 'payu.views.buy_order', name='payment'),
    url(r'^bookhotel/', 'hotels.views.userdetails', name='userdetails'),
        
    #=============================BUS URL=========================#
    url(r'^searchbus/', 'bus.views.search_bus', name='search_bus'),
    url(r'^seat_map/', 'bus.views.seat_map', name='seat_map'),
    url(r'^cancelpolicy/', 'bus.views.cancelpolicy', name='cancelpolicy'),
    url(r'^cancelticket/', 'bus.views.cancelticket', name='cancelticket'),
    url(r'^confirmbooking/', 'bus.views.confirmbooking', name='confirmbooking'),
    url(r'^bookingstatus/', 'bus.views.bookingstatus', name='bookingstatus'),
    url(r'^tentativebooking/', 'bus.views.tentativebooking', name='tentativebooking'),	
)
