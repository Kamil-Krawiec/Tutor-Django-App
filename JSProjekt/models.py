from django.db import models
from django.contrib.auth.models import User

# class TutorInfo(models.Model):
#     tutor = models.ForeignKey(User, on_delete=models.CASCADE)
#     primary_subject = models.CharField('Main subject you teach',max_length=100)
#     secondary_subject = models.CharField('Secound subject you teach',max_length=100)
#     availability = models.IntegerField('Working hours per week', default=0)
# 
#     REQUIRED_FIELDS = ['primary_subject']


class Mentee(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    name_surname = models.CharField('Name and surname of your client',max_length=200)
    info = models.TextField('Usefull informations about client', blank=True)
    price = models.IntegerField(default=0)
    starting_date = models.DateTimeField('When the lesson begins',help_text="%Y-%m-%d %H:%M")
    end_date = models.DateTimeField('When the lesson ends',help_text="%Y-%m-%d %H:%M")

    def __str__(self):
        return self.name_surname + " -> " + self.info
