from core.models import UserProfile
from django import forms
from django.contrib.auth.models import User

#in forms.py
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile