from django.conf.urls import patterns, include, url
from core import views

urlpatterns = patterns('',
    url(r'^ajax_login/', views.ajax_login, name='ajax_login'),
    url(r'^ajax_logout/', views.ajax_logout, name='ajax_logout'),
)