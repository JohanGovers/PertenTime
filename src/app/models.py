from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=256, unique=True)
    
    def __unicode__(self):
        return self.name

class Department(models.Model):
    code = models.CharField(max_length=256, blank=False)
    
    name = models.CharField(max_length=256, blank=False)
    
    def __unicode__(self):
        return self.code + " - " + self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    department = models.ForeignKey(Department)
    submitted_until = models.DateField()
    
    def __unicode__(self):
        return self.user.username

# TODO: remove hard link to user
# TODO: Unique constraint on combination of user_profile, date and project
class TimeEntry(models.Model):
    date = models.DateField()
    hours = models.IntegerField(default=0)
    project = models.ForeignKey(Project)
    user_profile = models.ForeignKey(UserProfile)
    
    def __unicode__(self):
        return str(self.date) + ": " + str(self.hours) + " h"