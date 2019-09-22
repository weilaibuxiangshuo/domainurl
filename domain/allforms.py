from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=56, required=True)
    password = forms.CharField(min_length=5 ,max_length=12,required=True)

# class CaptchaTestForm(forms.Form):
