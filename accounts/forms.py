from django import forms
from accounts import models as accounts_models


class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField()
