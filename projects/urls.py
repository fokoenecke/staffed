from django.conf.urls import patterns, url

from projects import views

urlpatterns = patterns('',
    url(r'^$', views.project_list, name='project_list'),
    url(r'^(?P<project_id>\d+)', views.show_project, name='project_show'),

    url(r'^add/$', views.add_project, name='project_add'),
    url(r'^edit/(?P<project_id>\d+)', views.edit_project, name='project_edit'),
    url(r'^save/$', views.save_project, name='project_save'),
    
    url(r'^slots/$', views.slot_list, name='slots'),
    url(r'^slots/apply/$', views.apply_for_slot, name='apply'),
    
    url(r'^applications/$', views.applications, name='application_list'),
    url(r'^applications/accept/$', views.apply_application, name='application_approve'),
    url(r'^applications/decline/$', views.decline_application, name='application_decline'),
    
)
