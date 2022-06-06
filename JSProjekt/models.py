from django.db import models
from django.contrib.auth.models import User


class Mentee(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    name_surname = models.CharField(max_length=200)
    info = models.CharField(max_length=200)
    price = models.IntegerField()
    starting_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return self.name_surname + " -> " + self.info
