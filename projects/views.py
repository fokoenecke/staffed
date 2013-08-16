from core.models import Skill
from core.views import index
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson
from django.views.decorators.csrf import ensure_csrf_cookie
from forms import ProjectForm
from projects.models import Project, Slot
from core.models import Skillset
import logging

@ensure_csrf_cookie
def project_list(request):
    if request.user.is_authenticated():
        project_list = Project.objects.all().select_related()
        context = {'project_list': project_list}
        return render(request, 'projects/list.html', context)
    else:
        return index(request)

@ensure_csrf_cookie
def slot_list(request):
    if request.user.is_authenticated():
        slot_list = Slot.objects.all().select_related()
        context = {'slot_list': slot_list}
        return render(request, 'projects/slot_list.html', context)
    else:
        return index(request)
    
@ensure_csrf_cookie
def add_project(request):
        
    if request.user.is_authenticated():
        data = {}
        data['project_form'] = ProjectForm()
        data['skill_list'] = Skill.objects.all()
        
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
            data['skill_list'] = Skill.objects.all()
        
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
      
    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST)
        if project_form.is_valid():
            
            logger.error(request.user.profile);
            
            project_id = request.POST.get('project_id')
            if project_id:
                project = Project.objects.get(pk=project_id)
            else: 
                project = project_form.save(commit=False)
            
            project.owner = request.user.profile
            slot_list = request.POST.get('slot_list');
            jsn = simplejson.loads(slot_list)
            
            project.save()    
            for slot in jsn:
                
                logger.error(slot)
                if "id" in slot:
                    project_slot = Slot.objects.get(pk=slot['id'])
                    slot_skillset = project_slot.skillset
                else:
                    project_slot = Slot()
                    project_slot.project = project
                    slot_skillset = Skillset()
                           
                skills = slot['skills']
                
                for skill in skills:
                    slot_nr = skill['slot']
                    if Skill.objects.filter(pk=skill['id']).exists():
                        skillset_skill = Skill.objects.get(pk=skill['id'])
                        slot_skillset.attach_skill(slot_nr, skillset_skill)
                
                slot_skillset.save()        
                project_slot.skillset = slot_skillset
                logger.error(project_slot) 
                logger.error(project_slot.skillset) 
                project_slot.save()
            
            some_data['return'] = 'true'
        else:
            some_data['error'] = "invalid input"
    
    data = simplejson.dumps(some_data)
    return HttpResponse(data, mimetype='application/json')