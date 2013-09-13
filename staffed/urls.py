from core import views
from core.views import index, profile, register, profile_list
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'login.views.home', name='home'),
    # url(r'^login/', include('login.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #TODO: hier nur links auf die module
    # Uncomment the next line to enable the admin:
    url(r'^$', index, name='index'),
    url(r'^profile/(?P<profile_id>\d+)', views.pub_profile, name='pub_profile'),
    url(r'^profile/assign_skill/', views.assign_skill_to_skillset, name='assign_skill'),
    url(r'^ajax/get_color/', views.get_color_code_from_skills, name='get_color'),
    url(r'^profile/', profile, name='profile'),
    url(r'^profiles/', profile_list, name='profile_list'),
    url(r'^projects/', include('projects.urls')),
    url(r'^register/', register, name='register'),
    url(r'^login/', include('core.urls')),
    url(r'^profile_skills/', views.get_profile_skills, name='profile_skills'),
    url(r'^test/', views.test, name='test'),
    
    url(r'^admin/', include(admin.site.urls)),
    (r'^favicon\.ico$', RedirectView.as_view(url= '/static/img/favicon.ico')),
)+ static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()