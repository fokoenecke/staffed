from core.models import UserProfile
from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["matriculation_nr", "first_name", "last_name", "studies"]