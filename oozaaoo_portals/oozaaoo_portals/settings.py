
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'a9u!!&(z!(fx9di_eh3aa0ujsvy71wf)3_e+nc@#(gr25(j@jr'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	# 'social_auth',
	'hotels',
    'bus',
    'payu',
    'transaction',
    'flight',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


ROOT_URLCONF = 'oozaaoo_portals.urls'

WSGI_APPLICATION = 'oozaaoo_portals.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',    # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'travelportal',                        # Or path to database file if using sqlite3.
        'USER': 'root',                          # Not used with sqlite3.
        'PASSWORD': 'root',                      # Not used with sqlite3.
        'HOST': 'localhost',                     # Set to empty string for localhost. Not used with sqlite3.
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = 'static_files'

STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__), '../static'),)

TEMPLATE_DIRS = os.path.join((os.path.dirname(__file__)), 'templates')

MEDIA_ROOT = '/media/'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    # 'social_auth.context_processors.social_auth_by_name_backends',
    # 'social_auth.context_processors.social_auth_backends',
    # 'social_auth.context_processors.social_auth_by_type_backends',
    # 'social_auth.context_processors.social_auth_login_redirect',
)

AUTHENTICATION_BACKENDS = (
#    'social_auth.backends.twitter.TwitterBackend',
     'social_auth.backends.facebook.FacebookBackend',
#    'social_auth.backends.google.GoogleOAuthBackend',
#    'social_auth.backends.google.GoogleOAuth2Backend',
#    'social_auth.backends.google.GoogleBackend',
#    'social_auth.backends.yahoo.YahooBackend',
#    'social_auth.backends.browserid.BrowserIDBackend',
#    'social_auth.backends.contrib.linkedin.LinkedinBackend',
#    'social_auth.backends.contrib.disqus.DisqusBackend',
#    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
#    'social_auth.backends.contrib.orkut.OrkutBackend',
#    'social_auth.backends.contrib.foursquare.FoursquareBackend',
#    'social_auth.backends.contrib.github.GithubBackend',
#    'social_auth.backends.contrib.vk.VKOAuth2Backend',
#    'social_auth.backends.contrib.live.LiveBackend',
#    'social_auth.backends.contrib.skyrock.SkyrockBackend',
#    'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
#    'social_auth.backends.contrib.readability.ReadabilityBackend',
#    'social_auth.backends.contrib.fedora.FedoraBackend',
#    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL          = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

FACEBOOK_APP_ID=''
FACEBOOK_API_SECRET=''
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'testmail123sample@gmail.com'
EMAIL_HOST_PASSWORD = 'testmail123'
EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

PAYU_INFO = {
             'merchant_key': "gtKFFx",
             'merchant_salt': "eCwWELxi",
             # for production environment use 'https://secure.payu.in/_payment'
             'payment_url': 'https://test.payu.in/_payment',
             #success url for hotel
             'surl':'http://localhost:8000/v2/setprovisionalbooking/',
             #success url for bus
             'surl1':'http://localhost:8000/v2/confirm/',
             #success url for flight
             'surl_flight':'http://localhost:8000/FlightConfirm/',
             'furl':'http://localhost:8000/failure/',
             'curl':'http://localhost:8000/cancel/',
            }

BUS_BASE="https://www.goibibobusiness.com/api/bus/"

HOTEL_BASE="https://www.goibibobusiness.com/api/hotels/b2b/"

FLIGHT_BASE="https://www.goibibobusiness.com/api/"

API_USERNAME="itsupport@oozaaoo.com"

API_PASSWORD="test123"

PAYMENT_SALT = "test123"

AMOUNT_CRYPT = "temp"
