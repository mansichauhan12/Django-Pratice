
from rest_framework.views import exception_handler

def custom_exception_handler(exc,context):
    response=exception_handler(exc,context)

    if response is not None:
        response.data={
            "success":False,
            "status_code":response.status_code,
            "errors":response.data
        }
    return response



# Your custom_exception_handler only formats exceptions that DRF knows how to handle.

# For example:

# ValidationError ✅
# NotFound / Http404 ✅
# PermissionDenied ✅
# AuthenticationFailed ✅
# unexpected Python errors like TypeError, NameError ❌ → these normally remain server errors and should be handled separately/logged.