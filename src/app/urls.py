from django.conf.urls import patterns, url
from app import views, report_view

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^get_time_entries$', views.get_time_entries, name='get_time_entries'),
        url(r'^save_time_entry$', views.save_time_entry, name='save_time_entry'),
        url(r'^set_last_submitted$', views.set_last_submitted, name='set_last_submitted'),
        url(r'^mark_project_as_favourite$', views.mark_project_as_favourite, name='mark_project_as_favourite'),
        url(r'^remove_project_as_favourite$', views.remove_project_as_favourite, name='remove_project_as_favourite'),
        url(r'^report/$', report_view.report, name='report'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),)
