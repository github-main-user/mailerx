from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "country"]
        exclude = ["password"]
