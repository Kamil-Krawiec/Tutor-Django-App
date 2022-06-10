from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import MenteeForm, SignUpForm
from .models import Mentee, Tutor


def home(request):
    return render(request, 'main/home.html')


def aboutPage(request):
    return render(request, 'main/aboutPage.html')


@login_required(login_url="/login")
def accountDetails(request):
    mentees = Mentee.objects.all()
    tutor_info = Tutor.objects.get(user=request.user)

    return render(request, 'main/account.html', {"mentees": mentees, "user": request.user, "tutor": tutor_info})


@login_required(login_url="/login")
def defineMentee(request):
    if request.method == 'POST':
        form = MenteeForm(request.POST)
        if form.is_valid():
            mentee = form.save(commit=False)
            mentee.tutor = request.user
            mentee.save()
            return redirect("/account")
    else:
        form = MenteeForm()

    return render(request, 'main/defineMentee.html', {"form": form})


def showTutors(request):
    general = request.GET.get('search_by')
    specified_main_subject = request.GET.get('main_subject')
    specified_second_subject = request.GET.get('second_subject')
    specified_name = request.GET.get('tutors_name')

    if specified_main_subject:
        tutors = Tutor.objects.filter(primary_subject__contains=specified_main_subject)
    elif specified_second_subject:
        tutors = Tutor.objects.filter(secondary_subject__contains=specified_second_subject)
    elif specified_name:
        tutors = Tutor.objects.filter(Q(user__first_name__contains=specified_name) |
                                      Q(user__last_name__contains=specified_name))
    elif general:
        tutors = Tutor.objects.filter(
            Q(user__first_name__contains=general) |
            Q(user__last_name__contains=general) |
            Q(primary_subject__contains=general) |
            Q(secondary_subject__contains=general)
        )
    else:
        tutors = None

    return render(request, 'main/tutors.html', {"tutors": tutors})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.tutor.primary_subject = form.cleaned_data.get('primary_subject')
            user.tutor.secondary_subject = form.cleaned_data.get('secondary_subject')
            user.tutor.availability = form.cleaned_data.get('availability')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('/home')
    else:
        form = SignUpForm()
    return render(request, 'registration/sign_up.html', {'form': form})
