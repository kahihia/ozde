from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^register', 'hotels.views.registration', name='registration'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'', include('social_auth.urls')),
	url(r'^$', 'hotels.views.home', name='home'),
    url(r'^getcity/', 'hotels.views.getcitylist', name='getcitylist'),
    url(r'^gethotellist/', 'hotels.views.gethotellist', name='gethotellist'),
    url(r'^gethoteldetails/', 'hotels.views.gethoteldetails', name='gethoteldetails'),    
    url(r'^bookhotel/', 'hotels.views.setprovisionalbooking', name='bookhotel'),
    url(r'^confirmbooking/', 'hotels.views.confirmbooking', name='confirmbooking'),
    url(r'^getbookstatus/', 'hotels.views.getbookingstatus', name='getbookingstatus'),
    url(r'^getbookdetails/', 'hotels.views.getbookingdetails', name='getbookingdetails'),
    url(r'^loadcitylist/', 'hotels.views.loadcitylist', name='loadcitylist'),
    url(r'^getrefund/', 'hotels.views.getrefund', name='getrefund'),
    url(r'^confirmcancel/', 'hotels.views.confirmcancel', name='confirmcancel'),	
)
