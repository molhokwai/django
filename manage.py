#!/usr/bin/env python
"Django's command-line utility for administrative tasks."
import os,sys
def main():
	'Run administrative tasks.';os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_app.settings')
	try:from django.core.management import execute_from_command_line as A
	except ImportError as B:raise ImportError("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?")from B
	A(sys.argv)
if __name__=='__main__':main()