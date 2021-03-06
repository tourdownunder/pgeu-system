from django.views.decorators.csrf import csrf_exempt

import postgresqleu.auth

from .decorators import global_login_exempt


# Wrap the API endpoint and remove the requirement for global http
# basic auth.
@global_login_exempt
@csrf_exempt
def auth_api(*args, **kwargs):
    return postgresqleu.auth.auth_api(*args, **kwargs)
