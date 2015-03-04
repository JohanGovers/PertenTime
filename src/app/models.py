from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    code = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    
    def __str__(self):
        return self.code + " - " + self.name

class Department(models.Model):
    code = models.CharField(max_length=256, blank=False)
    
    name = models.CharField(max_length=256, blank=False)
    
    def __str__(self):
        return self.code + " - " + self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    department = models.ForeignKey(Department)
    submitted_until = models.DateField()
    
    def __str__(self):
        return self.user.username

# TODO: remove hard link to user
# TODO: Unique constraint on combination of user_profile, date and project
class TimeEntry(models.Model):
    date = models.DateField()
    hours = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    project = models.ForeignKey(Project)
    userprofile = models.ForeignKey(UserProfile)
    
    def __str__(self):
        return str(self.date) + ": " + str(self.hours) + " h"