"""
Django settings for django_app project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from shutil import which
import os, logging, sys
from datetime import timedelta


# -----------------------------------------
# ______________________
# PRINTING
# Verbosity: 0 | 1 | 2 | 3
# ------------------------
PRINT_VERBOSITY = 0
def _print(val, VERBOSITY=0):
    if PRINT_VERBOSITY > 0:
        print(val)
    elif PRINT_VERBOSITY >= VERBOSITY:
        print(val)


# -----------------------------------------
# ______________________
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# -----------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
_print('--------------| BASE_DIR :: %s' % BASE_DIR, VERBOSITY=2)

sys.path.append(BASE_DIR) 



# for completing path on Pythonanywhere...
# -----------------------------------------
MAIN_APP_PATHNAME = ""
if str(BASE_DIR).find("/home/amylovesdaisys/") >= 0:
    MAIN_APP_PATHNAME = "django_app"


# -----------------------------------------
# ______________________
# QUICK-START DEVELOPMENT SETTINGS - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
# -----------------------------------------



# -----------------------------------------
# ______________________
# GLOBAL KEYS + SECURITY
# 
# WARNING: keep the secret key used in production secret!
#   1- Set environenent (with dotenv locally, 
#      with cli for apphost -like heroku...
#   2- Use:
#
#       SECRET_KEY = str(os.getenv('SECRET_KEY'))
# -----------------------------------------
SECRET_KEY = 'django-insecure-kc45@neob5bj2m#jj5_#^#eqz!htt#bg0hi4v)n1obnsmmy(zn'

# -----------------------------------------
# ______________________
# SECURITY WARNING: don't run with debug turned on in production!
# -----------------------------------------

DEBUG = False
IS_LIVE = True
IS_LOCAL = False
IS_HEROKU = os.environ.get('DYNO') is not None
IS_PYANY = str(BASE_DIR).find("/home/amylovesdaisys") >= 0
IS_REMOTE = str(BASE_DIR).find("/root/webscraper") >= 0

WHICH_ENV = 'LOCAL' if str(BASE_DIR).find('/home/nkensa/GDrive-local/Tree') == 0 else 'LIVE'
if WHICH_ENV == 'LOCAL' :
    DEBUG = True
    IS_LIVE = False
    IS_LOCAL = True

TESTING = "test" in sys.argv

# ---------------------
# 'postgres' or 'sqlite'
# ---------------------
WHICH_DATABASE = 'postgres'

# ---------------------
# 'Database', 'Redis' (must be installed), 
#  or 'CoreRedis' (must be tested, and installed? check documentation...)
# ---------------------
WHICH_CACHE = 'Database'

# ---------------------
# 'Db_logger' (must be installed) or 'File'
# ---------------------
WHICH_LOGGING = 'Db_logger'


# ---------------
# IPS, ALLOWED_HOSTS = ["127.0.0.1", "localhost", "nkensa.pythonanywhere.com"]
# ---------------
ALLOWED_HOSTS = ["87.106.66.163", "127.0.0.1", "localhost", "nkensa.pythonanywhere.com"]
INTERNAL_IPS = [
    "127.0.0.1",
]

# ---------------
# ______________________
# APPLICATION DEFINITION
# Application, Root Url, Middleware, Database, Cache
# ---------------

INSTALLED_APPS = [
    # core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # extensions
    'django_unicorn',
    'django_browser_reload',
    'tailwind',
    'theme',
    'fontawesomefree',
    # -----------------
    # @ToDo :: Fix pandas install on pythonanywhere to restore code (see all "Fix pandas" todos)
    # 'pandas',
    'selenium',
    'django_db_logger',

    # apps
    'django_app',
    'app',
    'webscraping',
]

if IS_LOCAL:
    INSTALLED_APPS += [
    ]

ROOT_URLCONF = 'django_app.urls'


# ---------------
# MIDDLEWARES
# ---------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

MIDDLEWARE.append('django_app.middleware.append_context.AppendContextMiddleware')
MIDDLEWARE.append('django_app.middleware.default_image.DefaultImageMiddleware')


# ---------------
# TEMPLATES
# ---------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ---------------
# WSGI
# ---------------
WSGI_APPLICATION = 'django_app.wsgi.application'
if IS_HEROKU:
    WSGI_APPLICATION = 'django_app.wsgi.app'


# --------
# DATABASE
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# --------

if WHICH_DATABASE == 'sqlite':
    # SQLITE
    # ------
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db/db.sqlite3',
        }
    }
    # ------

elif WHICH_DATABASE == 'postgres':
    # POSTGRES
    # --------
    os.environ.setdefault("PGDATABASE", "webscraper")
    os.environ.setdefault("PGUSER", "postgres")
    os.environ.setdefault("PGPASSWORD", "LeA45Jf~7ZL][e%k")
    os.environ.setdefault("PGHOST", "localhost")
    os.environ.setdefault("PGPORT", "5432")


    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get("PGDATABASE", "webscraper"),
            'USER': os.environ.get("PGUSER", "postgres"),
            'PASSWORD': os.environ.get("PGPASSWORD", ""),
            'HOST': os.environ.get("PGHOST", "localhost"),
            'PORT': os.environ.get("PGPORT", "5432"),
        }
    }

    if IS_HEROKU:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(conn_max_age=600)  # Optional connection pooling
        }
    # ------

# -----
# CACHE
# -----

if WHICH_CACHE == 'CoreRedis':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        }
    }

elif WHICH_CACHE == 'Redis':
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/1',  # Use the appropriate Redis server URL
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

elif WHICH_CACHE == 'Database':
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "django_cache",
        }
    }


# -------------------
# SESSION
#
# Optional: This is to ensure Django sessions are stored in Redis if used
# -------------------
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'



# -------------------
# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
# -------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = "journal"  # Redirect after login
LOGOUT_REDIRECT_URL = "journal"  # Redirect after logout


# -------------------
# INTERNATIONALIZATION
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# --------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# -------------------------------------------------
# STATIC & MEDIA FILES
#   CSS, JavaScript, Images...
#   https://docs.djangoproject.com/en/4.2/howto/static-files/
# -------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"
# STATICFILES_DIRS += [os.path.join(BASE_DIR, "media")]


if IS_HEROKU:
    STATIC_URL = 'https://webscraper-automat-d453797748a5.herokuapp.com/static/'
    MEDIA_URL = 'https://webscraper-automat-d453797748a5.herokuapp.com/media/'



# -------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# -------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -------------
# __________________
# OTHER APPS SETTINGS
# -------------


# ------------------------
# DJANGO-UNICORN
# ------------------------
UNICORN = {
    "MORPHER": {
        "NAME": "alpine",
    }
}


# ------------------------
# TAILWIND
# https://django-tailwind.readthedocs.io/
# https://django-tailwind.readthedocs.io/en/latest/installation.html
# ------------------------
TAILWIND_APP_NAME = 'theme'

# ------------------------
# NODE, NPM
# NPM_BIN_PATH = '/home/nkensa/.config/nvm/versions/node/v20.11.0/bin/npm'
# ------------------------
NPM_BIN_PATH = which("npm")


# ------------------------
# TAGGIT
# ------------------------
TAGGIT_CASE_INSENSITIVE = True
TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING = True


# ------------------------
# Mimetypes
# ------------------------
import mimetypes

mimetypes.add_type("application/javascript", ".js", True)
mimetypes.add_type("text/css", ".css", True)


# ------------------------
# WEBSCRAPER
# ------------------------
#
# Configuration
#    Caching duration: 15 mns
# ____________________
# cron scripts to setup:
# - webscraping cron
# - NOT REQUIRED, implememented with bash background 
#   task sleep and kill:
#       _________________
#       kill dangling check_tasks every 20 mns
#       actually kills all running tasks
#
#       * * * * * ~/@webscraper/scripts/webscraping_cron_exec
#       */10 * * * * pkill -f "check_tasks"
# ------------------------

#WEBSCRAPER_GECKODRIVER_BINARY_PATH = "/usr/bin/geckodriver-v0.30.0
WEBSCRAPER_GECKODRIVER_BINARY_PATH = "/usr/bin/geckodriver"
WEBSCRAPER_FIREFOX_BINARY_PATH = "/usr/lib/firefox/firefox"
WEBSCRAPER_SOURCE_PATH = "webscraping/modules/webscraper/"
WEBSCRAPER_HEADLESS = True
WEBSCRAPER_CACHING_DURATION = 600 # This should match THREAD_TIMEOUT, as a higher value would be inneffective...? 
WEBSCRAPER_THREADS_MAX = 10

# ------------------------------------------
# ChromeDriver, GeckoDriver: 
#   https://stackoverflow.com/questions/53603429/chromedriver-is-too-slower\
#                               -than-geckodriver-on-the-first-page-query-through-sele
#   O to not set a max RAM limitation
# ------------------------------------------
WEBSCRAPER_THREAD_MAX_RAM_KB = 0 # 1000000
WEBSCRAPER_THREAD_TIMEOUT = timedelta(minutes=10)  # Stop after 10 minutes
WEBSCRAPER_THREAD_TIMEOUT_FROM_CREATION = timedelta(minutes=30)  # Use `created_on` if `thread_task_started_at` not_available
WEBSCRAPER_TASK_MAX_ATTEMPTS = 3
WEBSCRAPER_THREADS_MAX_CHECK_TASK_TIME = 600 # Maximum check_task time before suppression
WEBSCRAPER_TASKHANDLER_CACHE_KEY = "task_dispatcher.taskHandler"

# ------------------------
# AI JOURNAL GUIDANCE
# ------------------------
#
# Configuration
# ------------------------

AI_JOURNAL_GUIDANCE_CHAT_HISTORY_RECALL = 50


# ------------------------
# LOGGING, PRINTING
# ------------------------

if WHICH_LOGGING == 'Db_logger':

    # ------------------------
    # DB LOGGER
    # ------------------------
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(asctime)s %(message)s'
            },
        },
        'handlers': {
            'db_log': {
                'level': 'DEBUG',
                'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
            },
        },
        'loggers': {
            'db': {
                'handlers': ['db_log'],
                'level': 'DEBUG',
                'formatter': 'simple'
            },
            'django.request': { # logging 500 errors to database
                'handlers': ['db_log'],
                'level': 'ERROR',
                'propagate': False,
                'formatter': 'simple'
            }
        }
    }

    # ---------------
    # Create a logger
    # ---------------
    logger = logging.getLogger('db')


if WHICH_LOGGING == 'File':

    # ------------------------
    # FILE LOGGING
    # ------------------------

    # Create a logger
    # ---------------
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the base logger level to DEBUG (captures all levels)


    # Create formatters
    # -----------------
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create handlers for each log level
    # ---------------
    debug_handler = logging.FileHandler('log/debug.log')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    info_handler = logging.FileHandler('log/info.log')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    warning_handler = logging.FileHandler('log/warning.log')
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(formatter)

    error_handler = logging.FileHandler('log/error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    critical_handler = logging.FileHandler('log/critical.log')
    critical_handler.setLevel(logging.CRITICAL)
    critical_handler.setFormatter(formatter)

    # Add handlers to the logger
    # ---------------
    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)
    logger.addHandler(critical_handler)



# ---------------
# BREAKPOINT LOG
# Utility to debug on a remote server...
#
# ______
# Requires:
#   logger
#
# ______
# Usage:
#
# - import `breakpoint_log` from your main app: 
# - Declare and assign `breakpoint_log_i`: 
# - Call `breakpoint_log()` at chosen breakpoints
# - Check logger ingo output to see where code breaks...
# 
#   ```python
#       from django_app.settings import breakpoint_log
#
#       breakpoint_log_i = 0
#       ...
#       breakpoint_log()  
#       ...
#       breakpoint_log()  
#       ...
#       breakpoint_log()
#       ...  
#   ```
# ---------------
breakpoint_log_i = 0
def breakpoint_log():
    global breakpoint_log_i
    breakpoint_log_i += 1
    logger.info(f"breakpoint_log: {breakpoint_log_i}")



# ---------------
# DJANGO TOOLBAR
# https://django-debug-toolbar.readthedocs.io/
# ---------------
if not TESTING:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        # "debug_toolbar",
    ]
    MIDDLEWARE = [
        # "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]

if False:
    # ----------------------
    # For configuration
    # ----------------------
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.history.HistoryPanel',
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.alerts.AlertsPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]

    # ----------------------
    # DEBUG_TOOLBAR_CONFIG
    # See:
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    # ----------------------





