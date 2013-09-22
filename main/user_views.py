from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

import pytz

from main.forms import MyUserCreate

def login_view(request):
    if request.user.is_authenticated():
        messages.error(request, 'You are already logged in')
        return HttpResponseRedirect(request.GET.get('next', '/'))
    if request.method == "POST":
        uname, pword = request.POST.get('uname'), request.POST.get('pword')
        user = authenticate(username=uname, password=pword)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have been logged in')
            else:
                return render(request, 'main/login.html', {'error_message': 'That user is inactive!'})
        else:
            return render(request, 'main/login.html', {'error_message': 'Incorrect username/password combo.'})
        return HttpResponseRedirect(request.GET.get('next', '/'))
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == "POST":
        form = MyUserCreate(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User was created successfully. Please sign in.")
            return HttpResponseRedirect('/')
        return render(request, 'main/signup.html', {'errors': form.errors, 'timezones': pytz.common_timezones})
    return render(request, 'main/signup.html', {'timezones': pytz.common_timezones})

@login_required
def change_location(request):
    if request.method == "POST":
        p = request.user.user_profile
        p.location = request.POST.get('location')
        p.geo_lat = request.POST.get('lat')
        p.geo_lon = request.POST.get('lon')
        p.save()
        messages.info(request, 'Location successfully added')
        if request.GET.get('next'):
            return HttpResponseRedirect(request.GET.get('next'))
        return HttpResponseRedirect(reverse('main:user_profile'))  # should be profile detail
    return render(request, 'main/location_pick.html')

@login_required
def user_profile(request):
    return render(request, 'main/user_profile.html')

def finish_change_pass(request):
    messages.success(request, 'Password reset successfully')
    return HttpResponseRedirect('/')
