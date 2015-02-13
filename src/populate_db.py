import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PertenTime.settings')

import django
django.setup()

from datetime import datetime, date
from django.contrib.auth.models import User
from app.models import Project, Department, UserProfile, TimeEntry

from app.model_helpers import add_department, add_project, add_time_entry, add_user

def populate():
    support = add_project('X', 'Support')
    invisible_screen = add_project('0', 'Invisible screen')
    DA_7250 = add_project('725', 'DA 7250')
    add_project('12', 'Cooling')
    
    software_department = add_department('7', 'Software')
    add_department('8', 'Construction')
    electronicts_department = add_department('9', 'Electronics')
    force_users_department = add_department('2', 'Force users')
    
    johan = add_user('jgovers', 'asdfasdf', 'Johan', 'Govers', 'johan@mail.com', software_department, date(2015, 1, 18))
    jane = add_user('jdoe', 'asdfasdf', 'Jane', 'Doe', 'jane@mail.com', software_department, date(2015, 1, 18))
    
    yoda = add_user('myoda', 'asdfasdf', 'Master', 'Yoda', 'yoda@mail.com', force_users_department, date(2015, 1, 11))
    luke = add_user('lskywalker', 'asdfasdf', 'Luke', 'Skywalker', 'luke@mail.com', force_users_department, date(2015, 1, 11))
    
    batman = add_user('batman', 'asdfasdf', 'Bat', 'Man', 'batman@gotham.com', electronicts_department, date(2015, 1, 1))

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

if __name__ == '__main__':
    print "Starting project population script..."
    populate()
