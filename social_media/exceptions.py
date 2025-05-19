from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied, ValidationError
from django.http import Http404

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response
    
    # Start with a generic structure 
    custom_response = {}

    # handle validation error (400)
    if isinstance(exc, ValidationError):
        errors = response.data
        flat_messages = []
        for filed, msgs in errors.items():
            for msg in msgs:
                flat_messages.append(f"{filed} filed is {msg.lower()}")
        custom_response["message"] = flat_messages[0] if flat_messages else "Invalid input"

    # Handle permission denied (403)
    elif isinstance(exc, PermissionDenied):
        custom_response["message"] = "you do not have permission to perform this action"
    
    # handle Not Found (404)
    elif isinstance(exc, Http404):
        custom_response["message"] = "Resource not found"

    else:
        custom_response["message"] = str(exc.detail) if hasattr(exc, 'detail') else str(exc)

    # Set the modified response
    response.data = custom_response
    return response