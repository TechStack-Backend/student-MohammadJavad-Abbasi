from functools import wraps
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

def owner_required(model, owner_field="owner", pk_kwarg="pk"):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *arg, **kwargs):
            obj = get_object_or_404(model, pk=kwargs[pk_kwarg])

            if getattr(obj, owner_field) != request.user:
                raise PermissionDenied
            
            return view_func(request, *arg, **kwargs)
        return _wrapped_view
    return decorator


