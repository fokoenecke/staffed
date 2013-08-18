from django.contrib.auth.forms import AuthenticationForm
from core.models import Skill

def login_form(request):
    return {'login_form': AuthenticationForm()}

def skill_list(request):
    return {'skill_list': Skill.objects.all()} 