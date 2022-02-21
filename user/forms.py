from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    class Meta:
        User = get_user_model()
        model = User
        fields = ['username', 'email', 'password1', 'password2']
