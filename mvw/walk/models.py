from django.db import models
from django.contrib.auth.models import User


class Walk(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    walkDate = models.DateField()
    distance = models.IntegerField()
    minutes = models.IntegerField()

    def __str__(self):
        return f"{self.user} - {self.walkDate} - {self.distance}Km - {self.minutes}min."


class VisitingPoint(models.Model):
    name = models.CharField(max_length=50)
    order_no = models.IntegerField()
    km = models.IntegerField()
    picture_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


"""
William Mackie Park - 01_wmp.png
"""