from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import FormView

User = get_user_model()


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("mailings:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
