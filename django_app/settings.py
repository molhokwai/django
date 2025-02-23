"\nDjango settings for django_app project.\n\nGenerated by 'django-admin startproject' using Django 4.2.11.\n\nFor more information on this file, see\nhttps://docs.djangoproject.com/en/4.2/topics/settings/\n\nFor the full list of settings and their values, see\nhttps://docs.djangoproject.com/en/4.2/ref/settings/\n"
_d='formatter'
_c='format'
_b='static'
_a='staticfiles'
_Z='journal'
_Y='LOCATION'
_X='PGPORT'
_W='localhost'
_V='PGHOST'
_U='PGPASSWORD'
_T='PGUSER'
_S='webscraper'
_R='PGDATABASE'
_Q='ENGINE'
_P='OPTIONS'
_O='Db_logger'
_N='Database'
_M='sqlite'
_L='django_app'
_K='level'
_J='db_log'
_I='simple'
_H='handlers'
_G='postgres'
_F='LOCAL'
_E='BACKEND'
_D=False
_C='NAME'
_B='default'
_A=True
from pathlib import Path
from shutil import which
import os,logging,sys
from datetime import timedelta
PRINT_VERBOSITY=0
def _print(val,VERBOSITY=0):
	if PRINT_VERBOSITY>0:print(val)
	elif PRINT_VERBOSITY>=VERBOSITY:print(val)
BASE_DIR=Path(__file__).resolve().parent.parent
_print('--------------| BASE_DIR :: %s'%BASE_DIR,VERBOSITY=2)
sys.path.append(BASE_DIR)
MAIN_APP_PATHNAME=''
if str(BASE_DIR).find('/home/amylovesdaisys/')>=0:MAIN_APP_PATHNAME=_L
SECRET_KEY='django-insecure-kc45@neob5bj2m#jj5_#^#eqz!htt#bg0hi4v)n1obnsmmy(zn'
DEBUG=_D
IS_LIVE=_A
IS_LOCAL=_D
IS_HEROKU=os.environ.get('DYNO')is not None
WHICH_ENV=_F if str(BASE_DIR).find('/home/nkensa/GDrive-local/Tree/')==0 else'LIVE'
if WHICH_ENV==_F:DEBUG=_A;IS_LIVE=_D;IS_LOCAL=_A
TESTING='test'in sys.argv
WHICH_DATABASE=_M
WHICH_CACHE=_N
WHICH_LOGGING=_O
ALLOWED_HOSTS=['*']
INTERNAL_IPS=['127.0.0.1']
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','django_unicorn','django_browser_reload','tailwind','theme','fontawesomefree','selenium','django_db_logger',_L,'app','webscraping']
if IS_LOCAL:INSTALLED_APPS+=[]
ROOT_URLCONF='django_app.urls'
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django_app.middleware.default_image.DefaultImageMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware','django_browser_reload.middleware.BrowserReloadMiddleware']
TEMPLATES=[{_E:'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':_A,_P:{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='django_app.wsgi.application'
if IS_HEROKU:WSGI_APPLICATION='django_app.wsgi.app'
if WHICH_DATABASE==_M:DATABASES={_B:{_Q:'django.db.backends.sqlite3',_C:BASE_DIR/'db/db.sqlite3'}}
elif WHICH_DATABASE==_G:
	os.environ.setdefault(_R,_S);os.environ.setdefault(_T,_G);os.environ.setdefault(_U,'LeA45Jf~7ZL][e%k');os.environ.setdefault(_V,_W);os.environ.setdefault(_X,'5432');DATABASES={_B:{_Q:'django.db.backends.postgresql',_C:os.environ.get(_R,_S),'USER':os.environ.get(_T,_G),'PASSWORD':os.environ.get(_U,''),'HOST':os.environ.get(_V,_W),'PORT':os.environ.get(_X,'5432')}}
	if WHICH_ENV!=_F or IS_HEROKU:import dj_database_url;DATABASES={_B:dj_database_url.config(conn_max_age=600)}
if WHICH_CACHE=='CoreRedis':CACHES={_B:{_E:'django.core.cache.backends.redis.RedisCache'}}
elif WHICH_CACHE=='Redis':CACHES={_B:{_E:'django_redis.cache.RedisCache',_Y:'redis://127.0.0.1:6379/1',_P:{'CLIENT_CLASS':'django_redis.client.DefaultClient'}}}
elif WHICH_CACHE==_N:CACHES={_B:{_E:'django.core.cache.backends.db.DatabaseCache',_Y:'django_cache'}}
SESSION_ENGINE='django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS=_B
AUTH_PASSWORD_VALIDATORS=[{_C:'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{_C:'django.contrib.auth.password_validation.MinimumLengthValidator'},{_C:'django.contrib.auth.password_validation.CommonPasswordValidator'},{_C:'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LOGIN_REDIRECT_URL=_Z
LOGOUT_REDIRECT_URL=_Z
LANGUAGE_CODE='en-us'
TIME_ZONE='UTC'
USE_I18N=_A
USE_TZ=_A
STATIC_URL='/static/'
STATIC_ROOT=BASE_DIR/_a
STATIC_ROOT=os.path.join(BASE_DIR,_a)
STATICFILES_DIRS=[os.path.join(BASE_DIR,_b)]
MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR/'media'
STATICFILES_DIRS=[BASE_DIR/_b,BASE_DIR/'media']
if IS_HEROKU:STATIC_URL='https://webscraper-automat-d453797748a5.herokuapp.com/static/';MEDIA_URL='https://webscraper-automat-d453797748a5.herokuapp.com/media/'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
UNICORN={'MORPHER':{_C:'alpine'}}
TAILWIND_APP_NAME='theme'
NPM_BIN_PATH=which('npm')
TAGGIT_CASE_INSENSITIVE=_A
TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING=_A
import mimetypes
mimetypes.add_type('application/javascript','.js',_A)
mimetypes.add_type('text/css','.css',_A)
WEBSCRAPER_SOURCE_PATH='webscraping/modules/webscraper/'
WEBSCRAPER_HEADLESS=_A
WEBSCRAPER_CACHING_DURATION=600
WEBSCRAPER_THREADS_MAX=2
WEBSCRAPER_THREAD_MAX_RAM_KB=0
WEBSCRAPER_THREAD_TIMEOUT=timedelta(minutes=10)
WEBSCRAPER_THREAD_TIMEOUT_FROM_CREATION=timedelta(minutes=30)
WEBSCRAPER_TASK_MAX_ATTEMPTS=3
WEBSCRAPER_THREADS_MAX_CHECK_TASK_TIME=600
WEBSCRAPER_TASKHANDLER_CACHE_KEY='task_dispatcher.taskHandler'
AI_JOURNAL_GUIDANCE_CHAT_HISTORY_RECALL=50
if WHICH_LOGGING==_O:LOGGING={'version':1,'disable_existing_loggers':_A,'formatters':{'verbose':{_c:'%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'},_I:{_c:'%(levelname)s %(asctime)s %(message)s'}},_H:{_J:{_K:'DEBUG','class':'django_db_logger.db_log_handler.DatabaseLogHandler'}},'loggers':{'db':{_H:[_J],_K:'DEBUG',_d:_I},'django.request':{_H:[_J],_K:'ERROR','propagate':_D,_d:_I}}};logger=logging.getLogger('db')
if WHICH_LOGGING=='File':logger=logging.getLogger(__name__);logger.setLevel(logging.DEBUG);formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s');debug_handler=logging.FileHandler('log/debug.log');debug_handler.setLevel(logging.DEBUG);debug_handler.setFormatter(formatter);info_handler=logging.FileHandler('log/info.log');info_handler.setLevel(logging.INFO);info_handler.setFormatter(formatter);warning_handler=logging.FileHandler('log/warning.log');warning_handler.setLevel(logging.WARNING);warning_handler.setFormatter(formatter);error_handler=logging.FileHandler('log/error.log');error_handler.setLevel(logging.ERROR);error_handler.setFormatter(formatter);critical_handler=logging.FileHandler('log/critical.log');critical_handler.setLevel(logging.CRITICAL);critical_handler.setFormatter(formatter);logger.addHandler(debug_handler);logger.addHandler(info_handler);logger.addHandler(warning_handler);logger.addHandler(error_handler);logger.addHandler(critical_handler)
if not TESTING:INSTALLED_APPS=[*INSTALLED_APPS];MIDDLEWARE=[*MIDDLEWARE]
if _D:DEBUG_TOOLBAR_PANELS=['debug_toolbar.panels.history.HistoryPanel','debug_toolbar.panels.versions.VersionsPanel','debug_toolbar.panels.timer.TimerPanel','debug_toolbar.panels.settings.SettingsPanel','debug_toolbar.panels.headers.HeadersPanel','debug_toolbar.panels.request.RequestPanel','debug_toolbar.panels.sql.SQLPanel','debug_toolbar.panels.staticfiles.StaticFilesPanel','debug_toolbar.panels.templates.TemplatesPanel','debug_toolbar.panels.alerts.AlertsPanel','debug_toolbar.panels.cache.CachePanel','debug_toolbar.panels.signals.SignalsPanel','debug_toolbar.panels.redirects.RedirectsPanel','debug_toolbar.panels.profiling.ProfilingPanel']