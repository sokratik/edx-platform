import json
import os


from .common import *
from logsettings import get_logger_config
from os.path import expanduser


ENV_ROOT = REPO_ROOT.dirname()  # virtualenv dir /mitx is in
CONFIG_ROOT = path(expanduser("~")) / "sokratik-infra/json-configs"

# specified as an environment variable.  Typically this is set
# in the service's upstart script and corresponds exactly to the service name.
# Service variants apply config differences via env and auth JSON files,
# the names of which correspond to the variant.
SERVICE_VARIANT = os.environ.get('SERVICE_VARIANT', "lms")



# when not variant is specified we attempt to load an unvaried
# config set.
CONFIG_PREFIX = ""

if SERVICE_VARIANT:
    CONFIG_PREFIX = SERVICE_VARIANT + "."


############### ALWAYS THE SAME ################################
DEBUG = False
TEMPLATE_DEBUG = False

EMAIL_BACKEND = 'django_ses.SESBackend'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

###################################### CELERY  ################################

# Don't use a connection pool, since connections are dropped by ELB.
BROKER_POOL_LIMIT = 0
BROKER_CONNECTION_TIMEOUT = 1

# For the Result Store, use the django cache named 'celery'
CELERY_RESULT_BACKEND = 'cache'
CELERY_CACHE_BACKEND = 'celery'

# When the broker is behind an ELB, use a heartbeat to refresh the
# connection and to detect if it has been dropped.
BROKER_HEARTBEAT = 10.0
BROKER_HEARTBEAT_CHECKRATE = 2

# Each worker should only fetch one message at a time
CELERYD_PREFETCH_MULTIPLIER = 1

# Skip djcelery migrations, since we don't use the database as the broker
SOUTH_MIGRATION_MODULES = {
    'djcelery': 'ignore',
}

# Rename the exchange and queues for each variant

QUEUE_VARIANT = CONFIG_PREFIX.lower()

CELERY_DEFAULT_EXCHANGE = 'edx.{0}core'.format(QUEUE_VARIANT)

HIGH_PRIORITY_QUEUE = 'edx.{0}core.high'.format(QUEUE_VARIANT)
DEFAULT_PRIORITY_QUEUE = 'edx.{0}core.default'.format(QUEUE_VARIANT)
LOW_PRIORITY_QUEUE = 'edx.{0}core.low'.format(QUEUE_VARIANT)

CELERY_DEFAULT_QUEUE = DEFAULT_PRIORITY_QUEUE
CELERY_DEFAULT_ROUTING_KEY = DEFAULT_PRIORITY_QUEUE

CELERY_QUEUES = {
    HIGH_PRIORITY_QUEUE: {},
    LOW_PRIORITY_QUEUE: {},
    DEFAULT_PRIORITY_QUEUE: {}
}


############# NON-SECURE ENV CONFIG ##############################
# Things like server locations, ports, etc.
with open(CONFIG_ROOT / CONFIG_PREFIX + "env.json") as env_file:
    ENV_TOKENS = json.load(env_file)


EMAIL_BACKEND = ENV_TOKENS.get('EMAIL_BACKEND', EMAIL_BACKEND)
EMAIL_FILE_PATH = ENV_TOKENS.get('EMAIL_FILE_PATH', None)
LMS_BASE = ENV_TOKENS.get('LMS_BASE')

SITE_NAME = ENV_TOKENS['SITE_NAME']


SESSION_ENGINE = ENV_TOKENS.get('SESSION_ENGINE', SESSION_ENGINE)
SESSION_COOKIE_DOMAIN = ENV_TOKENS.get('SESSION_COOKIE_DOMAIN')

# allow for environments to specify what cookie name our login subsystem should use
# this is to fix a bug regarding simultaneous logins between edx.org and edge.edx.org which can
# happen with some browsers (e.g. Firefox)
if ENV_TOKENS.get('SESSION_COOKIE_NAME', None):
    # NOTE, there's a bug in Django (http://bugs.python.org/issue18012) which necessitates this being a str()
    SESSION_COOKIE_NAME = str(ENV_TOKENS.get('SESSION_COOKIE_NAME'))

BOOK_URL = ENV_TOKENS['BOOK_URL']
MEDIA_URL = ENV_TOKENS['MEDIA_URL']
LOG_DIR = ENV_TOKENS['LOG_DIR']
CACHES = ENV_TOKENS['CACHES']
DEFAULT_FROM_EMAIL = ENV_TOKENS.get('DEFAULT_FROM_EMAIL', DEFAULT_FROM_EMAIL)
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get('DEFAULT_FEEDBACK_EMAIL', DEFAULT_FEEDBACK_EMAIL)
ADMINS = ENV_TOKENS.get('ADMINS', ADMINS)
SERVER_EMAIL = ENV_TOKENS.get('SERVER_EMAIL', SERVER_EMAIL)
TECH_SUPPORT_EMAIL = ENV_TOKENS.get('TECH_SUPPORT_EMAIL', TECH_SUPPORT_EMAIL)
CONTACT_EMAIL = ENV_TOKENS.get('CONTACT_EMAIL', CONTACT_EMAIL)
BUGS_EMAIL = ENV_TOKENS.get('BUGS_EMAIL', BUGS_EMAIL)
MANAGERS = ADMINS
#Theme overrides
THEME_NAME = ENV_TOKENS.get('THEME_NAME', None)
if not THEME_NAME is None:
    enable_theme(THEME_NAME)
    FAVICON_PATH = 'themes/%s/images/favicon.ico' % THEME_NAME
#static files location
STATIC_ROOT = ENV_TOKENS.get('STATIC_ROOT')
# Marketing link overrides
MKTG_URL_LINK_MAP.update(ENV_TOKENS.get('MKTG_URL_LINK_MAP', {}))

#Timezone overrides
TIME_ZONE = ENV_TOKENS.get('TIME_ZONE', TIME_ZONE)

#Additional installed apps
for app in ENV_TOKENS.get('ADDL_INSTALLED_APPS', []):
    INSTALLED_APPS += (app,)

for feature, value in ENV_TOKENS.get('MITX_FEATURES', {}).items():
    MITX_FEATURES[feature] = value

WIKI_ENABLED = ENV_TOKENS.get('WIKI_ENABLED', WIKI_ENABLED)
local_loglevel = ENV_TOKENS.get('LOCAL_LOGLEVEL', 'INFO')
LOGGING = get_logger_config(LOG_DIR,
                            logging_env=ENV_TOKENS['LOGGING_ENV'],
                            syslog_addr=(ENV_TOKENS['SYSLOG_SERVER'], 5140),
                            local_loglevel=local_loglevel,
                            debug=False,
                            service_variant=SERVICE_VARIANT)

COURSE_LISTINGS = ENV_TOKENS.get('COURSE_LISTINGS', {})
SUBDOMAIN_BRANDING = ENV_TOKENS.get('SUBDOMAIN_BRANDING', {})
VIRTUAL_UNIVERSITIES = ENV_TOKENS.get('VIRTUAL_UNIVERSITIES', [])
META_UNIVERSITIES = ENV_TOKENS.get('META_UNIVERSITIES', {})
COMMENTS_SERVICE_URL = ENV_TOKENS.get("COMMENTS_SERVICE_URL", '')
COMMENTS_SERVICE_KEY = ENV_TOKENS.get("COMMENTS_SERVICE_KEY", '')
CERT_QUEUE = ENV_TOKENS.get("CERT_QUEUE", 'test-pull')
ZENDESK_URL = ENV_TOKENS.get("ZENDESK_URL", None)
FEEDBACK_SUBMISSION_EMAIL = ENV_TOKENS.get("FEEDBACK_SUBMISSION_EMAIL")
MKTG_URLS = ENV_TOKENS.get('MKTG_URLS', MKTG_URLS)

for name, value in ENV_TOKENS.get("CODE_JAIL", {}).items():
    oldvalue = CODE_JAIL.get(name)
    if isinstance(oldvalue, dict):
        for subname, subvalue in value.items():
            oldvalue[subname] = subvalue
    else:
        CODE_JAIL[name] = value

COURSES_WITH_UNSAFE_CODE = ENV_TOKENS.get("COURSES_WITH_UNSAFE_CODE", [])

MITX_FEATURES['ENABLE_DISCUSSION_HOME_PANEL'] = ENV_TOKENS.get('ENABLE_DISCUSSION_HOME_PANEL', True)

MITX_FEATURES['USE_DJANGO_PIPELINE'] = True
PIPELINE = True

# Celery Broker
CELERY_BROKER_TRANSPORT = ENV_TOKENS.get("CELERY_BROKER_TRANSPORT", "")
CELERY_BROKER_HOSTNAME = ENV_TOKENS.get("RABBIT_HOST", "")
CELERY_BROKER_VHOST = ENV_TOKENS.get("RABBIT_VHOST", "")

############################## SECURE AUTH ITEMS ###############
# Secret things: passwords, access keys, etc.

with open(CONFIG_ROOT / CONFIG_PREFIX + "auth.json") as auth_file:
    AUTH_TOKENS = json.load(auth_file)

############### Mixed Related(Secure/Not-Secure) Items ##########
# If Segment.io key specified, load it and enable Segment.io if the feature flag is set
SEGMENT_IO_LMS_KEY = AUTH_TOKENS.get('SEGMENT_IO_LMS_KEY')
if SEGMENT_IO_LMS_KEY:
    MITX_FEATURES['SEGMENT_IO_LMS'] = ENV_TOKENS.get('SEGMENT_IO_LMS', False)

SECRET_KEY = AUTH_TOKENS['SECRET_KEY']
AWS_ACCESS_KEY_ID = AUTH_TOKENS["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = AUTH_TOKENS["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = AUTH_TOKENS.get('AWS_STORAGE_BUCKET_NAME', 'euthyphro')
DATABASES = AUTH_TOKENS['DATABASES']
XQUEUE_INTERFACE = AUTH_TOKENS['XQUEUE_INTERFACE']
# Get the MODULESTORE from auth.json, but if it doesn't exist,
# use the one from common.py
MODULESTORE = AUTH_TOKENS.get('MODULESTORE', MODULESTORE)
CONTENTSTORE = AUTH_TOKENS.get('CONTENTSTORE', CONTENTSTORE)

OPEN_ENDED_GRADING_INTERFACE = AUTH_TOKENS.get('OPEN_ENDED_GRADING_INTERFACE',
                                               OPEN_ENDED_GRADING_INTERFACE)

# Analytics dashboard server
ANALYTICS_SERVER_URL = ENV_TOKENS.get("ANALYTICS_SERVER_URL", "")
ANALYTICS_API_KEY = AUTH_TOKENS.get("ANALYTICS_API_KEY", "")

# Zendesk
ZENDESK_USER = AUTH_TOKENS.get("ZENDESK_USER")
ZENDESK_API_KEY = AUTH_TOKENS.get("ZENDESK_API_KEY")

# API Key for inbound requests from Notifier service
EDX_API_KEY = AUTH_TOKENS.get("EDX_API_KEY")

CELERY_BROKER_USER = AUTH_TOKENS.get("CELERY_BROKER_USER", "")
CELERY_BROKER_PASSWORD = AUTH_TOKENS.get("CELERY_BROKER_PASSWORD", "")

BROKER_URL = "{0}://{1}:{2}@{3}/{4}".format(CELERY_BROKER_TRANSPORT,
                                            CELERY_BROKER_USER,
                                            CELERY_BROKER_PASSWORD,
                                            CELERY_BROKER_HOSTNAME,
                                            CELERY_BROKER_VHOST)



