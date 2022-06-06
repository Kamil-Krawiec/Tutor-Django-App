from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request,'main/home.html')

def aboutPage(request):
    return render(request,'main/aboutPage.html')


@login_required(login_url="/login")
def accountDetails(request):
    return render(request, 'main/account.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')

    else:
        form = RegistrationForm()

    return render(request,'registration/sign_up.html',{"form": form})