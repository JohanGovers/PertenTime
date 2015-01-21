from django.contrib.auth.models import User
from app.models import Project, Department, UserProfile, TimeEntry

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