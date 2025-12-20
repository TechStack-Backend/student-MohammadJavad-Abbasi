from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from . import models

class OwnerOrPermissionMixin:
    owner_field = "user"
    permission_required = None
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if getattr(obj, self.owner_field) == request.user:
            return super().dispatch(request, *args, **kwargs)
        
        if self.permission_required and request.user.has_perm(self.permission_required):
            return super().dispatch(request, *args, **kwargs)
        
        raise PermissionDenied
    

class OwnerAssignMixin:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class SkillOwnerOrPermissionMixin:
    
    permission_required = None
    developer_kwarg = 'dev_id'

    def dispatch(self, request, *args, **kwargs):
        dev_id = kwargs.get(self.developer_kwarg)

        if dev_id:
            self.developer = get_object_or_404(models.Developer, pk=dev_id)

            if self.permission_required and request.user.has_perm(self.permission_required):
                return super().dispatch(request, *args, **kwargs)

            if not hasattr(request.user, "developer"):
                raise PermissionDenied

            if self.developer.user != request.user:
                raise PermissionDenied

        else:
            if self.permission_required and not request.user.has_perm("crud.add_skill"):
                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
    
    
class SkillObjectOwnerOrPermissionMixin:
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.permission_required and request.user.has_perm(self.permission_required):
            return super().dispatch(request, *args, **kwargs)

        if self.object.developer.user == request.user:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied
