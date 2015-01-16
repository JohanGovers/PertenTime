import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PertenTime.settings')

import django
django.setup()

from datetime import datetime, date
from django.contrib.auth.models import User
from app.models import Project, Department, UserProfile, TimeEntry

def populate():
    support = add_project('Support')
    invisible_screen = add_project('Invisible screen')
    DA_7250 = add_project('DA 7250')
    add_project('Cooling')
    
    software_department = add_department('7', 'Software')
    add_department('8', 'Construction')
    add_department('9', 'Electronics')
    force_users_department = add_department('2', 'Force users')
    
    johan = add_user('jgovers', 'asdfasdf', 'Johan', 'Govers', 'johan@mail.com', software_department, date(2015, 1, 18))
    jane = add_user('jdoe', 'asdfasdf', 'Jane', 'Doe', 'jane@mail.com', software_department, date(2015, 1, 18))
    
    yoda = add_user('myoda', 'asdfasdf', 'Master', 'Yoda', 'yoda@mail.com', force_users_department, date(2015, 1, 11))
    luke = add_user('lskywalker', 'asdfasdf', 'Luke', 'Skywalker', 'luke@mail.com', force_users_department, date(2015, 1, 11))

    add_time_entry(support, johan, date(2015, 1, 2), 8)
    
    add_time_entry(DA_7250, johan, date(2015, 1, 5), 8)
    add_time_entry(DA_7250, johan, date(2015, 1, 6), 8)
    add_time_entry(DA_7250, johan, date(2015, 1, 7), 8)
    add_time_entry(DA_7250, johan, date(2015, 1, 8), 8)
    add_time_entry(DA_7250, johan, date(2015, 1, 9), 8)
    
    add_time_entry(DA_7250, johan, date(2015, 1, 12), 8)
    add_time_entry(DA_7250, johan, date(2015, 1, 13), 8)
    add_time_entry(DA_7250, johan, date(2015, 1, 14), 6)
    add_time_entry(support, johan, date(2015, 1, 14), 2)
    add_time_entry(DA_7250, johan, date(2015, 1, 14), 6)
    add_time_entry(DA_7250, johan, date(2015, 1, 15), 8)
    add_time_entry(DA_7250, johan, date(2015, 1, 16), 8)
    
    
    add_time_entry(DA_7250, jane, date(2015, 1, 2), 6)
    
    add_time_entry(DA_7250, jane, date(2015, 1, 5), 6)
    add_time_entry(DA_7250, jane, date(2015, 1, 6), 6)
    add_time_entry(DA_7250, jane, date(2015, 1, 7), 6)
    add_time_entry(DA_7250, jane, date(2015, 1, 8), 6)
    add_time_entry(DA_7250, jane, date(2015, 1, 9), 6)
    
    add_time_entry(DA_7250, jane, date(2015, 1, 12), 1)
    add_time_entry(DA_7250, jane, date(2015, 1, 13), 6)
    add_time_entry(DA_7250, jane, date(2015, 1, 14), 6)
    add_time_entry(DA_7250, jane, date(2015, 1, 15), 2)
    add_time_entry(DA_7250, jane, date(2015, 1, 16), 4)
    
    
    add_time_entry(invisible_screen, yoda, date(2015, 1, 2), 8)
    
    add_time_entry(invisible_screen, yoda, date(2015, 1, 5), 8)
    add_time_entry(invisible_screen, yoda, date(2015, 1, 6), 8)
    add_time_entry(invisible_screen, yoda, date(2015, 1, 7), 8)
    add_time_entry(invisible_screen, yoda, date(2015, 1, 8), 8)
    add_time_entry(invisible_screen, yoda, date(2015, 1, 9), 8)
    
    add_time_entry(invisible_screen, yoda, date(2015, 1, 12), 8)
    add_time_entry(invisible_screen, yoda, date(2015, 1, 13), 8)
    add_time_entry(invisible_screen, yoda, date(2015, 1, 14), 8)
    add_time_entry(invisible_screen, yoda, date(2015, 1, 15), 8)
    add_time_entry(invisible_screen, yoda, date(2015, 1, 16), 8)
    
    
    add_time_entry(invisible_screen, luke, date(2015, 1, 2), 8)
    
    add_time_entry(invisible_screen, luke, date(2015, 1, 5), 8)
    add_time_entry(invisible_screen, luke, date(2015, 1, 6), 8)
    add_time_entry(invisible_screen, luke, date(2015, 1, 7), 8)
    add_time_entry(invisible_screen, luke, date(2015, 1, 8), 8)
    add_time_entry(invisible_screen, luke, date(2015, 1, 9), 8)
    
    add_time_entry(invisible_screen, luke, date(2015, 1, 12), 8)
    add_time_entry(invisible_screen, luke, date(2015, 1, 13), 8)
    add_time_entry(invisible_screen, luke, date(2015, 1, 14), 8)
    add_time_entry(invisible_screen, luke, date(2015, 1, 15), 8)
    add_time_entry(invisible_screen, luke, date(2015, 1, 16), 8)

def add_project(name):
    print " - Add project " + name
    p = Project.objects.get_or_create(name=name)[0]
    return p

def add_department(code, name):
    print " - Add department " + code + " - " + name
    d = Department.objects.get_or_create(code=code, name=name)[0]
    return d

def add_user(username, password, first_name, last_name, email, department, submitted_until):
    try:
        u = User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        print " - Add user " + username
        u = User.objects.create_user(username=username, email=email, password=password)
    
    print " - Set properties on " + username
    u.set_password(password)
    u.email = email
    u.first_name = first_name
    u.last_name = last_name
    u.save()

    print " - Save user profile for " + username
    try:
        up = UserProfile.objects.get(user=u)
    except UserProfile.DoesNotExist:
        up = UserProfile(user=u)
    up.department = department
    up.submitted_until = submitted_until
    up.save()
    
    return up

def add_time_entry(project, user_profile, date, hours):
    print " - Add time entry " + str(project) + " - " + str(user_profile) + " " + str(date) + ": " + str(hours)
    e = TimeEntry.objects.get_or_create(project=project, user_profile=user_profile, date=date, hours=hours)[0]
    return e

if __name__ == '__main__':
    print "Starting project population script..."
    populate()
