from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primary_subject = models.CharField('Main subject you teach',blank=True,max_length=200)
    secondary_subject = models.CharField('Secound subject you teach', blank=True,max_length=200)
    availability = models.IntegerField('Working hours per week',blank=True,default=0)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Tutor.objects.create(user=instance)
        instance.tutor.save()

class Mentee(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    name_surname = models.CharField('Name and surname of your client',max_length=200)
    info = models.TextField('Usefull informations about client', blank=True)
    price = models.IntegerField(default=0)
    starting_date = models.DateTimeField('When the lesson begins',help_text="%Y-%m-%d %H:%M")
    end_date = models.DateTimeField('When the lesson ends',help_text="%Y-%m-%d %H:%M")

    def __str__(self):
        return self.name_surname + " -> " + self.info
