from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Mentee


class SignUpForm(UserCreationForm):
    primary_subject = forms.CharField(label='Main subject you teach', required=True, max_length=200)
    secondary_subject = forms.CharField(label='Secound subject you teach', required=False, max_length=200)
    availability = forms.IntegerField(label='Working hours per week', required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'primary_subject',
                  'secondary_subject', 'availability']


class MenteeForm(forms.ModelForm):
    class Meta:
        model = Mentee
        fields = ['name_surname', 'info', 'price', 'starting_date', 'starting_time', 'duration']
