from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sing_up'),
    path('aboutPage', views.aboutPage, name='aboutPage'),
    path('account', views.accountDetails, name='aboutPage'),
    path('addNewMentee', views.defineMentee, name='defineMentee'),
    path('findTutor', views.showTutors, name='showTutors'),
]

handler404 = 'JSProjekt.views.handle_not_found'
