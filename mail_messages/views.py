from typing import override

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.mixins import (
    ManagerCreateForbiddenMixin,
    OwnerRequiredMixin,
    RoleFilteredListMixin,
)

from .forms import MessageForm
from .models import Message


class MessageListView(LoginRequiredMixin, RoleFilteredListMixin, ListView):
    model = Message
    success_url = reverse_lazy("mail_messages:message_list")


class MessageCreateView(LoginRequiredMixin, ManagerCreateForbiddenMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mail_messages:message_list")

    @override
    def form_valid(self, form):
        message = form.instance
        message.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mail_messages:message_list")


class MessageDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mail_messages:message_list")
