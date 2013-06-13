from core.forms import UserProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import simplejson
from django.views.decorators.csrf import ensure_csrf_cookie
import logging


# Create your views here.
@ensure_csrf_cookie
def index(request):
    if request.method == 'POST': # If the form has been submitted...
        form = AuthenticationForm(data=request.POST) # A form bound to the POST data
        profile_form = UserProfileForm()
    else:
        form = AuthenticationForm() # An unbound form
        profile_form = UserProfileForm()

    return render(request, 'core/index.html', {'form': form, 'profile_form': profile_form})

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
    