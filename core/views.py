from core.forms import UserProfileForm
from core.models import Skill
from django import forms
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.http.request import QueryDict
from django.shortcuts import render
from django.utils import simplejson
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import logging

#TODO: Context_Processor login_form erstellen, damit nicht in jeder view die Login_Form uebergeben werden muss

@ensure_csrf_cookie
def index(request):
    if request.method == 'POST': # If the form has been submitted...
        login_form = AuthenticationForm(data=request.POST) # A form bound to the POST data
        profile_form = UserProfileForm()
    else:
        login_form = AuthenticationForm() # An unbound form
        profile_form = UserProfileForm()

    return render(request, 'core/index.html', {'login_form': login_form, 'profile_form': profile_form})

@ensure_csrf_cookie
def ajax_login(request):
    logger = logging.getLogger("django")    
    some_data = {'return': 'false'}         

    if request.method == 'POST':                                                                                                                                                                                              
        login_form = AuthenticationForm(data=request.POST)
        logger.error(login_form);              
        if login_form.is_valid():
            login(request, login_form.get_user())
            some_data = {'return': 'true'}
        else:
            some_data['error'] = "invalid login"

    data = simplejson.dumps(some_data)
    return HttpResponse(data, mimetype='application/json')

@ensure_csrf_cookie
def ajax_logout(request):
    logout(request)
    some_data = {'return': 'true'}
    data = simplejson.dumps(some_data)
    return HttpResponse(data, mimetype='application/json')


@ensure_csrf_cookie
def profile(request):
    
    if request.user.is_authenticated():
        data = {}
        user_profile = request.user.profile
        skillset = user_profile.skillset
        
        data['profile_form'] = UserProfileForm(instance=user_profile)
        data['login_form'] = AuthenticationForm()
        data['skill_list'] = Skill.objects.all()
        data['skillset'] = [skillset.skill1, skillset.skill2, skillset.skill3, skillset.skill4, skillset.skill5]
        
        print user_profile
        return render(request, 'core/profile.html', data)
    else:
        return index(request)
    

@ensure_csrf_cookie
def save_profile(request):
    logger = logging.getLogger("django") 
    some_data = {'return': 'false'}
    if request.method == 'POST':
        logger.error("test")
        profile_form = UserProfileForm(data=request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            logger.error(profile_form)
            profile_form.save()
            some_data['return'] = 'true'
        else:
            logger.error(profile_form.errors)
            some_data['error'] = "invalid input"
    
    data = simplejson.dumps(some_data)
    return HttpResponse(data, mimetype='application/json')

@ensure_csrf_cookie
def register(request):
    login_form = AuthenticationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
        
    return render(request, "core/register.html", {'form': form, 'login_form' : login_form, })

@ensure_csrf_cookie
def assign_skill_to_skillset(request):
    jsn = simplejson.loads(request.body)
    logger = logging.getLogger("django")

    skill_id = jsn['id']
    slot_nr = jsn['slot_nr']
    skill = Skill.objects.get(pk=skill_id)
    skillset = request.user.profile.skillset
    
    if slot_nr == 0:
        skillset.skill1 = skill
    elif slot_nr== 1:
        skillset.skill2 = skill
    elif slot_nr == 2:
        skillset.skill3 = skill
    elif slot_nr == 3:
        skillset.skill4 = skill
    elif slot_nr == 4:
        skillset.skill5 = skill
             
    skillset.save()
    some_data = {'return': 'true'}
    data = simplejson.dumps(some_data)
    
    return HttpResponse(data, mimetype='application/json')
    