from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *




class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class ProfileAuthenticationForm(AuthenticationForm):
    pass


class UpdateProfile(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email")



