from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import *
from models import *

# class EmailUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#
#     class Meta:
#         model = Person
#         fields = ("username", "first_name", "last_name", "phone", "email", "password1", "password2")
#
# class PersonForm(ModelForm):
#     class Meta:
#         model = Person
#
#
# class LikeForm(ModelForm):
#     class Meta:
#         model = Like
