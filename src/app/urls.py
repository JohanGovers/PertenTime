from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^get_time_entries$', views.get_time_entries, name='get_time_entries'),
        url(r'^create_time_post$', views.create_time_post, name='create_time_post'),
        url(r'^report/$', views.report, name='report'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),)