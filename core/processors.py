from django.contrib.auth.forms import AuthenticationForm
from core.models import Skill
from projects.models import Project

def login_form(request):
    return {'login_form': AuthenticationForm()}

def skill_list(request):
    return {'skill_list': Skill.objects.all().order_by('name')}

def application_num(request):
    applications = []
    if request.user.is_authenticated():
        
        projects = Project.objects.filter(owner = request.user.profile)
        slots = []
        
        for project in projects:
            for slot in project.slot_set.all():
                slots.append(slot)
        
        for slot in slots:
            for application in slot.application_set.all():
                if application.accepted is None:
                    applications.append(application)
    
    return {'application_num': len(applications)}
    