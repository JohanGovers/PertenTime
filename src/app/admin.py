from django.contrib import admin
from app.models import Project, TimeEntry, UserProfile, Department

admin.site.register(Project)
admin.site.register(TimeEntry)
admin.site.register(UserProfile)
admin.site.register(Department)