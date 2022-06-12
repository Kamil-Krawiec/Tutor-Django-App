from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import MenteeForm, SignUpForm
from django.core.mail import send_mail
from .models import Mentee, Tutor


def home(request):
    return render(request, 'main/home.html')


def aboutPage(request):
    return render(request, 'main/aboutPage.html')



@login_required(login_url="/login")
def accountDetails(request):
    mentees = Mentee.objects.all()
    tutor_info = Tutor.objects.get(user=request.user)

    if request.method == "POST":
        mentee_id = request.POST.get("mentee_id")
        mentee = Mentee.objects.filter(id=mentee_id).first()

        if mentee:
            messages.success(request, f'Mentee {mentee.name_surname} deleted successful!')
            user = request.user
            user.tutor.availability += mentee.duration
            user.save()
            mentee.delete()

    return render(request, 'main/account.html', {"mentees": mentees, "user": request.user, "tutor": tutor_info})


@login_required(login_url="/login")
def defineMentee(request):
    if request.method == 'POST':
        form = MenteeForm(request.POST)
        if form.is_valid():
            mentee = form.save(commit=False)
            user = request.user
            if user.tutor.availability - mentee.duration > 0:
                mentee.tutor = user
                mentee.save()
                user.tutor.availability -= mentee.duration
                user.save()
                messages.success(request, 'Success! The mentee was added correctly.')
                return redirect("/account")
            else:
                messages.error(request, 'Your weekly availability is too low!')
                return redirect('/account')
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

    if request.method== 'POST':
        form=request.POST
        sender = form.get('sender')
        recipients = [form.get('receiver')]
        subject = form.get('title')
        message = form.get('message')
        send_mail(subject, message, sender, recipients)



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
