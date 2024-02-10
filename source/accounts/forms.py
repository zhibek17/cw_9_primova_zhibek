from django import forms
from .models import *

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number']
