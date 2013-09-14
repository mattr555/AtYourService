from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.core.urlresolvers import reverse

from itertools import chain
from operator import attrgetter
from datetime import datetime

from main.forms import UserEventCreate
from main.models import Event, UserEvent, Organization

def home(request):
    return render(request, 'main/home.html')

def list_events_one(request):
    return list_events(request, 1)

@login_required
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
            set = Event.objects.filter(date_start__gte=timezone.now()).order_by('date_start')
    else:
        set = Event.objects.filter(date_start__gte=timezone.now()).order_by('date_start')

    for k in request.GET:
        if k == 'range':
            pass
        else:
            v = request.GET.get(k)
            if 'organization_id' in k:
                filters["Organization: " + str(Organization.objects.get(pk=v).name)] = k + '=' + v
            elif 'organization__name' in k:
                filters["Organization contains: " + v] = k + '=' + v
            elif 'name' in k:
                filters["Name contains: " + v] = k + '=' + v
            elif 'date' in k:
                if k == 'date_start__gte':
                    filters["Date after: " + v] = k + '=' + v
                elif k == 'date_start__lte':
                    filters["Date before: " + v] = k + '=' + v
                raw_date = v.split('/')
                v = datetime(int(raw_date[2]), int(raw_date[0]), int(raw_date[1]))
            filter_dict[k] = v
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
    recent_events = list(o.events.filter(date_start__gte=timezone.now()).order_by('date_start')[:5])
    return render(request, 'main/org_detail.html', {'organization': o, 'recent_events': recent_events})

@login_required
def userevent_detail(request, pk):
    e = get_object_or_404(UserEvent.objects, pk=pk)
    if request.user == e.user:
        return render(request, 'main/userevent_detail.html', {'userevent': e})
    messages.error(request, "That's not your event!")
    return HttpResponseRedirect('/')

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
def track_events(request):
    event = list(request.user.events.all())
    user_event = list(request.user.user_events.all())
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
