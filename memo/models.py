from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)  # Not Changable
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)   # This Foriegn Key Store Data into That Logged user
    # on_delete means Model deleted from signed user database

    def __str__(self):
        return self.title

    # One user can has lots of different to dos
    # but many to dos have single that particular user, ThereFore Here we use Foreign Key To Access Those Particular user


#  After then ---- GO To Admin.py to import these into admin
