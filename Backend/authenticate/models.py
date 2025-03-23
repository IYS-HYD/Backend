from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class Backend(models.Model):
    user = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

class SadhanaEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wake_up_time = models.TimeField()
    rounds_chanted = models.IntegerField()
    hours_studied_college = models.FloatField()
    card_filled_at = models.DateTimeField(default=now)
    day_rest = models.CharField(max_length=255)
    seva = models.CharField(max_length=255)
    cleanliness = models.CharField(max_length=255)
    book_reading_sp = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f"{self.user.username} - {self.card_filled_at}"