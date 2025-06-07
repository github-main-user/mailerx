from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import HttpResponseForbidden

User = get_user_model()


class ManagerCreateForbiddenMixin:
    """Forbids to create an object for managers."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == User.UserRole.MANAGER:
            return HttpResponseForbidden(b"Managers can't create objects")
        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin:
    """Forbids access if current user is not owner."""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return HttpResponseForbidden(b"You are not owner of this object")
        return super().dispatch(request, *args, **kwargs)


class RoleFilteredListMixin:
    """Provides filtering of queryset by user's role."""

    def get_queryset(self):
        qs = super().get_queryset()

        match self.request.user.role:
            case User.UserRole.MANAGER:
                user_pk = self.request.GET.get("user_pk")
                if user_pk:
                    # get objects for a specific owner
                    qs = qs.filter(owner__pk=user_pk)
            case User.UserRole.USER:
                qs = qs.filter(owner=self.request.user)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.user.role == User.UserRole.MANAGER:
            user_list = cache.get("user_list")

            if not user_list:
                user_list = User.objects.filter(role=User.UserRole.USER)
                cache.set("user_list", user_list, settings.CACHE_QS_TIME_SEC)

            context["user_list"] = user_list
        return context


class ManagerRoleRequiredMixin:
    """Forbids access if current user is not manager."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != User.UserRole.MANAGER:
            return HttpResponseForbidden(b"You are not a manager")
        return super().dispatch(request, *args, **kwargs)
