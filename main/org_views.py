from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

import datetime
import pytz

from main.models import Organization, Event
from main.forms import EventCreate

@login_required
def manage_home(request):
    if not request.user.user_profile.is_org_admin():
        messages.error(request, "You aren't an organization administrator!")
        return HttpResponseRedirect('/')
    return render(request, 'main/manage_home.html', {'organizations': request.user.orgs_admin.all()})

@login_required
def org_home(request, pk):
    o = get_object_or_404(Organization.objects, pk=pk)
    if not request.user.id == o.admin_id:
        messages.error(request, "You aren't authorized to do that!")
        return HttpResponseRedirect('/')
    events = o.events.order_by('-date_start')
    return render(request, 'main/org_home.html', {'org': o, 'events': events})

def validate_org(request, o):
    errors = []
    if request.POST.get('name'):
        o.name = request.POST.get('name')
    else:
        errors.append('A name is required')
    if request.POST.get('description'):
        o.description = request.POST.get('description')
    else:
        errors.append('A description is required')
    if request.POST.get('location'):
        o.location = request.POST.get('location')
    else:
        errors.append('A location is required')
    if request.POST.get('lat'):
        o.geo_lat = float(request.POST.get('lat'))
        o.geo_lon = float(request.POST.get('lon'))
    if errors:
        return (errors, o)
    o.save()
    return True

@login_required
def org_edit(request, pk):
    o = get_object_or_404(Organization.objects, pk=pk)
    if o not in request.user.orgs_admin.all():
        messages.error(request, "That's not your organization!")
        return HttpResponseRedirect(reverse('main:org_manage'))
    if request.method == "GET":
        return render(request, 'main/org_edit.html', {'org': o})
    else:
        err = validate_org(request, o)
        if isinstance(err, tuple):
            return render(request, 'main/org_edit.html', {'org': err[1], 'errors': err[0]})
        messages.success(request, 'Organization successfully edited')
        return HttpResponseRedirect(reverse('main:manage_home'))

@login_required
def org_new(request):
    if request.user.user_profile.is_org_admin():
        if request.method == "GET":
            return render(request, 'main/org_new.html')
        else:
            o = Organization(admin_id=request.user.id)
            err = validate_org(request, o)
            if isinstance(err, tuple):
                return render(request, 'main/org_new.html', {'org': err[1], 'errors': err[0]})
            messages.success(request, 'Organization successfully created')
            return HttpResponseRedirect(reverse('main:manage_home'))
    else:
        messages.error(request, "You aren't an organization administrator!")
        return HttpResponseRedirect('/')

@login_required
def org_delete(request, pk):
    o = Organization.objects.get(pk=pk)
    if o:
        if request.user.id == o.admin_id:
            o.delete()
            messages.info(request, "Organization successfully deleted")
        else:
            messages.error(request, "You aren't authorized to do that!")
    else:
        messages.error(request, "Organization not found!")
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET.get('next'))
    return HttpResponseRedirect('/')

@login_required
def event_home(request, pk):
    e = get_object_or_404(Event.objects, pk=pk)
    if request.user.id == e.organizer_id:
        user_statuses = []
        for u in e.participants.all():
            user_statuses.append([u, e.confirm_status(u)])
        return render(request, 'main/event_home.html', {'event': e, 'user_statuses': user_statuses})
    messages.error(request, "That's not your event!")
    return HttpResponseRedirect(reverse('main:manage_home'))

@login_required
def event_new(request):
    if request.method == "GET":
        return render(request, 'main/event_new.html')
    else:
        form = EventCreate(user=request.user, data=request.POST)
        if form.is_valid():
            e = form.save()
            messages.success(request, 'Event created successfully')
            return HttpResponseRedirect(reverse('main:event_home', args=(e.id)))
        else:
            return render(request, 'main/event_new.html', {'errors': form.errors, 'event': form})

@login_required
def event_edit(request, pk):
    e = get_object_or_404(Event.objects, pk=pk)
    if not request.user.id == e.organizer_id:
        messages.error(request, "You aren't authorized to do that!")
        return HttpResponseRedirect(reverse('main:manage_home'))
    if request.method == "GET":
        form = EventCreate(data=e.__dict__, user=request.user)
        return render(request, 'main/event_edit.html', {'event': form})
    else:
        data_dict = request.POST.dict()
        data_dict['organization'] = e.organization_id
        form = EventCreate(data=data_dict, user=request.user)
        if form.is_valid():
            for k, v in form.cleaned_data.items():
                if k != 'organization':
                    e.__dict__[k] = v
            e.save()
            messages.success(request, 'Event edited successfully')
            return HttpResponseRedirect(reverse('main:event_home', args=(str(e.id))))
        else:
            return render(request, 'main/event_edit.html', {'event': form, 'errors': form.errors})

@login_required
def event_delete(request, pk):
    e = Event.objects.get(pk=pk)
    if e:
        if request.user.id == e.organizer_id:
            e.delete()
            messages.info(request, "Event successfully deleted")
        else:
            messages.error(request, "You aren't authorized to do that!")
    else:
        messages.error(request, "Event not found!")
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET.get('next'))
    return HttpResponseRedirect('/')

