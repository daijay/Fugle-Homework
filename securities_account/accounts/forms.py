from django import forms
from django.contrib.auth.models import User

from .models import AccountApplication


class AccountApplicationForm(forms.ModelForm):
    class Meta:
        model = AccountApplication
        fields = ['account_name', 'phone', 'address']

