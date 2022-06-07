from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Mentee


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    primary_subject = forms.CharField(required=True, label='Main subject you teach')
    secondary_subject = forms.CharField(required=False, label='Secound subject you teach')
    availability = forms.CharField(required=False, label='Working hours per week')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'primary_subject',
                  'secondary_subject', 'availability']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.primary_subject = self.cleaned_data['primary_subject']
        user.secondary_subject = self.cleaned_data['secondary_subject']
        user.availability = self.cleaned_data['availability']

        if commit:
            user.save()

        return user


class MenteeForm(forms.ModelForm):
    class Meta:
        model = Mentee
        fields = ['name_surname', 'info', 'price', 'starting_date', 'end_date']
