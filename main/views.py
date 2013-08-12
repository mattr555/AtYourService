from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.core.urlresolvers import reverse

from itertools import chain
from operator import attrgetter

from main.forms import MyUserCreate, UserEventCreate
from main.models import Event, UserEvent, Organization

def home(request):
    return render(request, 'main/home.html')

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
        return render(request, 'main/signup.html', {'errors': form.errors})
    return render(request, 'main/signup.html')

def list_events_one(request):
    return list_events(request, 1)

def list_events(request, page):
    filter_dict, filters = {}, {}
    if request.GET.get('range'):
        if request.user.user_profile.geo_lat:
            dist = request.GET.get('range')
            set = Event.objects.within(request.user.user_profile, float(dist))
            set = set.filter(date_start__gte=timezone.now()).order_by('date_start')
            if float(dist) == 1.0:
                mi = ' mile'
            else:
                mi = ' miles'
            filters['Search radius: ' + request.GET.get('range') + mi] = 'range=' + dist
        else:
            messages.error(request, "You don't have a location set! <a href='/profile/change_loc?next=" + reverse('main:list_events') + "'>Set one now</a>",
                           extra_tags='safe')
    else:
        set = Event.objects.filter(date_start__gte=timezone.now()).order_by('date_start')

    for k in request.GET:
        if k == 'range':
            pass
        else:
            v = request.GET.get(k)
            filter_dict[k] = v
            if 'organization_id' in k:
                filters["Organization: " + str(Organization.objects.get(pk=v).name)] = k + '=' + v
            elif 'organization__name' in k:
                filters["Organization contains: " + v] = k + '=' + v
            elif 'name' in k:
                filters["Name contains: " + v] = k + '=' + v
        set = set.filter(**filter_dict)

    paginator = Paginator(set, 10, allow_empty_first_page=True)
    try:
        page_set = paginator.page(page)
    except PageNotAnInteger:
        page_set = paginator.page(1)
    except EmptyPage:
        messages.error(request, "That page was not found!")
        return HttpResponseRedirect('/')
    if not page_set.object_list:
        messages.error(request, "No events found!")
    return render(request, 'main/list_events.html', {'events': page_set, 'filters': filters})

class EventView(generic.DetailView):
    model = Event
    template = 'main/event_detail.html'

def organization_detail(request, pk):
    o = get_object_or_404(Organization.objects, pk=pk)
    recent_events = o.events.filter(date_start__gte=timezone.now()).order_by('date_start')[:5]
    return render(request, 'main/organization_detail.html', {'organization': o, 'recent_events': recent_events})

@login_required
def userevent_detail(request, pk):
    e = get_object_or_404(UserEvent.objects, pk=pk)
    if request.user == e.user:
        return render(request, 'main/userevent_detail.html', {'userevent': e})
    messages.error(request, "That's not your event!")
    return HttpResponseRedirect('/')

@login_required
def track_events(request):
    event = request.user.events.all()
    user_event = request.user.user_events.all()
    event_set = sorted(chain(event, user_event),
                       key=attrgetter('date_end'))
    total_hours = 0
    for i in event_set:
        total_hours += i.hours()

    if request.method == "POST":
        form = UserEventCreate(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully')
            return HttpResponseRedirect(reverse('main:track'))
        else:
            messages.error(request, 'Error creating event')
    else:
        form = UserEventCreate()
    return render(request, 'main/track_events.html', {'events': event_set,
                                                      'total_hours': total_hours,
                                                      'form': form})

@login_required
def delete_userevent(request, pk):
    event = UserEvent.objects.get(pk=pk)
    if event:
        if request.user == event.user:
            event.delete()
            messages.info(request, "Event successfully deleted")
        else:
            messages.error(request, "You aren't authorized to do that!")
    else:
        messages.error(request, "Event not found!")
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET.get('next'))
    return HttpResponseRedirect('/')

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
        return HttpResponseRedirect('/')  # should be profile detail
    return render(request, 'main/location_pick.html')
