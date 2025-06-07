from typing import override

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from core.mixins import (
    ManagerCreateForbiddenMixin,
    ManagerRoleRequiredMixin,
    OwnerRequiredMixin,
    RoleFilteredListMixin,
)
from mailings.tasks import send_started_mailings

from .forms import MailingForm
from .models import Mailing


class MailingListView(LoginRequiredMixin, RoleFilteredListMixin, ListView):
    model = Mailing
    success_url = reverse_lazy("mailings:mailing_list")

    @override
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # to compare start_time and end_time in the template
        context["now"] = timezone.now()
        return context


class MailingCreateView(LoginRequiredMixin, ManagerCreateForbiddenMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailing_list")

    @override
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    @override
    def form_valid(self, form):
        mailing = form.instance
        mailing.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailings:mailing_list")

    @override
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    @override
    def get_object(self, queryset=None):
        mailing = super().get_object(queryset)
        if mailing.status == Mailing.MailingStatus.FINISHED:
            raise PermissionDenied("You can't edit a finished mailing.")
        return mailing


class MailingDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailings:mailing_list")


class MailingStartView(LoginRequiredMixin, View):
    def post(self, request, pk: int):
        mailing = get_object_or_404(
            Mailing, pk=pk, owner=request.user, status=Mailing.MailingStatus.CREATED
        )

        mailing.status = Mailing.MailingStatus.STARTED
        mailing.save()
        return redirect("mailings:mailing_list")


class MailingsLaunchView(LoginRequiredMixin, ManagerRoleRequiredMixin, View):
    def post(self, request):
        send_started_mailings.delay()
        messages.success(request, "Mailings are launched ahead of schedule.")
        return redirect("mailings:mailing_list")


class MailingToggleStatus(LoginRequiredMixin, ManagerRoleRequiredMixin, View):
    def post(self, _request, pk: int):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_active = not mailing.is_active
        mailing.save()
        return redirect("mailings:mailing_list")
