from django.contrib.auth import get_user_model
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
        if self.request.user.role == User.UserRole.MANAGER:
            user_pk = self.request.GET.get("user_pk")
            if user_pk:
                qs = qs.filter(owner__pk=user_pk)
            return qs
        elif self.request.user.role == User.UserRole.USER:
            qs.filter(owner=self.request.user)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.user.role == User.UserRole.MANAGER:
            context["user_list"] = User.objects.filter(role=User.UserRole.USER)
        return context
