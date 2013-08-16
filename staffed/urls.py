from core import views
from core.views import index, profile, save_profile, register, profile_list
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'login.views.home', name='home'),
    # url(r'^login/', include('login.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', index, name='index'),
    url(r'^profile/(?P<profile_id>\d+)', views.pub_profile, name='pub_profile'),
    url(r'^profile/assign_skill/', views.assign_skill_to_skillset, name='assign_skill'),
    url(r'^profile/', profile, name='profile'),
    url(r'^profiles/', profile_list, name='profile_list'),
    url(r'^projects/', include('projects.urls')),
    url(r'^register/', register, name='register'),
    url(r'^save_profile/', save_profile, name='save_profile'),
    url(r'^login/', include('core.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()