from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


class SelfOrAdminMixin:
    permission_required = "auth.delete_user"

    def get_target_user(self):
        pk = self.kwargs.get("pk")

        if pk is None:
            return self.request.user

        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise PermissionDenied("User not found")

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")


        if pk is None:
            return super().dispatch(request, *args, **kwargs)
        
        user = get_object_or_404(User, pk=pk)

        if user == request.user:
            return super().dispatch(request, *args, **kwargs)

        if not request.user.has_perm(self.permission_required):
            raise PermissionDenied("Admin permission required")

        return super().dispatch(request, *args, **kwargs)


class UserObjectPermissionMixin:
    permission_required = "auth.view_user"

    def get_object(self, queryset=None):
        user = super().get_object(queryset)

        if user == self.request.user:
            return user

        if self.request.user.has_perm(self.permission_required):
            return user

        raise PermissionDenied("You do not have permission to view this profile")