from core.models import Skill
from core.views import index
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson
from django.views.decorators.csrf import ensure_csrf_cookie
from forms import ProjectForm
from projects.models import Project, Slot, Application
from core.models import Skillset
from core.helpers import rgb_difference
from django.contrib import messages
import logging


@ensure_csrf_cookie
def project_list(request):
    if request.user.is_authenticated():
        project_list = Project.objects.all().select_related().order_by('name')
        context = {'project_list': project_list}
        return render(request, 'projects/list.html', context)
    else:
        return index(request)    

@ensure_csrf_cookie
def slot_list(request):
    if request.user.is_authenticated():
        slot_list = Slot.objects.all().filter(user__isnull=True).select_related()
        
        logger = logging.getLogger("django")
        logger.error("test")
        
        if request.POST:
            logger.error("test2")
            jsn = simplejson.loads(request.body)
            color = jsn['color'];
        
            logger.error(color)
            for slot in slot_list:
                
                logger.error(rgb_difference(color, slot.skillset.get_color()))
                if rgb_difference(color, slot.skillset.get_color()) > 20:
                    logger.error("test3")
                    slot_list = slot_list.exclude(id=slot.id)
        
        
        logger.error(slot_list)
        context = {'slot_list': slot_list,
                   'skillset' : Skillset(),}
        if request.POST:
            return render(request, 'projects/slot_list_page.html', context)
        else: 
            return render(request, 'projects/slot_list.html', context)
    else:
        return index(request)
    
@ensure_csrf_cookie
def add_project(request):
        
    if request.user.is_authenticated():
        data = {}
        data['project_form'] = ProjectForm()
        
        return render(request, 'projects/new_project.html', data)
    else:
        return index(request)

@ensure_csrf_cookie
def edit_project(request, project_id):
    if request.user.is_authenticated():
        project = get_object_or_404(Project, pk=project_id)
        if project.owner == request.user.profile:
            data = {}
            data['project_form'] = ProjectForm(instance=project)
        
            return render(request, 'projects/new_project.html', data)
        else:
            return show_project(request, project_id)

@ensure_csrf_cookie
def show_project(request, project_id):
    if request.user.is_authenticated():
        project = get_object_or_404(Project, pk=project_id)
        
        #bsp fuer inline forms
        #projectSlots = inlineformset_factory(Project, Slot)
        #slotForms = projectSlots(instance=project)
        
        data = {}        
        data['project'] = project
        
        return render(request, 'projects/project.html', data)
    else:
        return index(request)
    
    
@ensure_csrf_cookie
def save_project(request):
    some_data = {'return': 'false'}
    logger = logging.getLogger("django")
    message = ''
    
    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST)
        if project_form.is_valid():
            
            logger.error(request.user.profile);
            
            project_id = request.POST.get('project_id')
            if project_id:
                project = Project.objects.get(pk=project_id)
                project.name = project_form.cleaned_data['name']
                project.description = project_form.cleaned_data['description']
                message = "Das Projekt " + project.name + " wurde erfolgreich gespeichert."
            else: 
                project = project_form.save(commit=False)
                message = "Das Projekt " + project.name + " wurde erfolgreich angelegt."
            
            project.owner = request.user.profile
            member_list = request.POST.get('member_list');
            jsn = simplejson.loads(member_list)
            
            project.save()    
            for member in jsn:
                
                logger.error(member)
                if "id" in member:
                    project_member = Slot.objects.get(pk=member['id'])
                    member_skillset = project_member.skillset
                else:
                    project_member = Slot()
                    project_member.project = project
                    member_skillset = Skillset()
                           
                slots = member['slots']
                
                for slot in slots:
                    slot_nr = slot['slot']
                    if "id" in slot:
                        if Skill.objects.filter(pk=slot['id']).exists():
                            skill = Skill.objects.get(pk=slot['id'])
                            member_skillset.attach_skill(slot_nr, skill)
                
                member_skillset.save()        
                project_member.skillset = member_skillset
                
                project_member.name = member['name']
                project_member.description = member['desc']
                
                logger.error(project_member) 
                logger.error(project_member.skillset) 
                project_member.save()
            
            some_data['return'] = 'true'
            some_data['project_id'] = project.id
            messages.success(request, message)
        else:
            some_data['error'] = project_form.errors
    
    data = simplejson.dumps(some_data)
    return HttpResponse(data, content_type='application/json')

@ensure_csrf_cookie
def apply_for_slot(request):
    slot_id = simplejson.loads(request.body)

    application = Application()
    application.slot = Slot.objects.get(pk=slot_id)
    application.applicant = request.user.profile
    application.save()

    messages.success(request, "Du hast dich erfolgreich als " + application.slot.name + " beworben!")
 
    some_data = {'return': 'true'}    
    data = simplejson.dumps(some_data)
    return HttpResponse(data, content_type='application/json')

@ensure_csrf_cookie
def applications(request):
    
    if request.user.is_authenticated():
        
        projects = Project.objects.filter(owner = request.user.profile)
        slots = []
        
        for project in projects:
            for slot in project.slot_set.all():
                slots.append(slot)
        
        applications = []
        for slot in slots:
            for application in slot.application_set.all():
                applications.append(application)
        
        context = {
            'application_list': applications,
        }
                    
        return render(request, 'projects/application.html', context)
    else:
        return index(request)
    
@ensure_csrf_cookie
def apply_application(request):
    application_id = simplejson.loads(request.body)
    
    application = Application.objects.get(pk=application_id)
    application.accepted = True
    
    slot = application.slot
    slot.user = application.applicant
    application.save()
    slot.save()

    some_data = {'return': 'true'}
    data = simplejson.dumps(some_data)
    return HttpResponse(data, content_type='application/json')
    
@ensure_csrf_cookie  
def decline_application(request):
    application_id = simplejson.loads(request.body)
    
    application = Application.objects.get(pk=application_id)
    application.accepted = False
    application.save()

    some_data = {'return': 'true'}
    data = simplejson.dumps(some_data)
    return HttpResponse(data, content_type='application/json')