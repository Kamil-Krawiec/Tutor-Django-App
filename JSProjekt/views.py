from django.shortcuts import render, redirect
from .forms import RegistrationForm, MenteeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Mentee,User



def home(request):
    return render(request, 'main/home.html')


def aboutPage(request):
    return render(request, 'main/aboutPage.html')


@login_required(login_url="/login")
def accountDetails(request):
    mentees = Mentee.objects.all()
    print()
    return render(request, 'main/account.html',{"mentees":mentees,})


@login_required(login_url="/login")
def defineMentee(request):
    if request.method == 'POST':
        form = MenteeForm(request.POST)
        if form.is_valid():
            mentee = form.save(commit=False)
            mentee.tutor = request.user
            mentee.save()
            return redirect("/account.html")
    else:
        form = MenteeForm()

    return render(request, 'main/defineMentee.html', {"form":form})


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('/home')

    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {"form": form})
