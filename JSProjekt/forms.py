from django import forms
from .models import Mentee, Tutor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    primary_subject = forms.CharField(label='Main subject you teach', required=True, max_length=200)
    secondary_subject = forms.CharField(label='Secound subject you teach', required=False, max_length=200)
    availability = forms.IntegerField(label='Working hours per week', required=False)
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2','primary_subject', 'secondary_subject', 'availability']


class MenteeForm(forms.ModelForm):
    class Meta:
        model = Mentee
        fields = ['name_surname', 'info', 'price', 'starting_date', 'starting_time','duration']


# class EmailForm(forms.Form):
#     receiver = forms.EmailField()
#     sender = forms.EmailField()
#     subject = forms.CharField(max_length=200)
#     message = forms.CharField(widget=forms.Textarea())
#
#
#     class Meta:
#         fields = ['receiver', 'sender','subject','message']

