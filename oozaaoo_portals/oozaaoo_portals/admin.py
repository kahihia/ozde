# Import the UserProfile model individually.
from django.contrib import admin
from hotels.models import citylist

admin.site.register(citylist)

