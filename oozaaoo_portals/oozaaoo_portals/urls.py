from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'hotels.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
	url(r'', include('social_auth.urls')),	
)
