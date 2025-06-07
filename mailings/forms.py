from django import forms

from .models import Mailing


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "clients"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # filter clients by owner
        if user and "clients" in self.fields:
            self.fields["clients"].queryset = self.fields["clients"].queryset.filter(
                owner=user
            )

        # filter messages by owner
        if user and "message" in self.fields:
            self.fields["message"].queryset = self.fields["message"].queryset.filter(
                owner=user
            )

        for field in ("start_time", "end_time"):
            if self.fields.get(field):
                self.fields[field].input_formats = ["%Y-%m-%dT%H:%M"]
