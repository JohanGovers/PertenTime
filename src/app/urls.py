from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^get_time_entries$', views.get_time_entries, name='get_time_entries'),
        url(r'^save_time_entry$', views.save_time_entry, name='save_time_entry'),
        url(r'^set_last_submitted$', views.set_last_submitted, name='set_last_submitted'),
        url(r'^report/$', views.report, name='report'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),)