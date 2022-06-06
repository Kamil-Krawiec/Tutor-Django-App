from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    primary_subject = forms.CharField(required=True,label='Main subject you teach')
    secondary_subject = forms.CharField(required=False,label = 'Secound subject you teach')
    availability = forms.CharField(required=False, label='Working hours per week')


    class Meta():
        model = User
        fields = ['username','email','password1','password2','primary_subject','secondary_subject','availability']