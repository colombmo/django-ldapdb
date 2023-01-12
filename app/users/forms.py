from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class InviteForm(forms.Form):
    email_address = forms.EmailField(max_length=150)

class CodeCheckForm(forms.Form):
    invite_code = forms.CharField(max_length=30)

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required = True, widget=forms.EmailInput(attrs={'class': 'validate',}))

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")