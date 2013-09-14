from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from main.models import Organization

@login_required
def manage_home(request):
    if not request.user.user_profile.is_org_admin:
        messages.error("You aren't an organization administrator!")
        return HttpResponseRedirect('/')
    return render(request, 'main/manage_home.html', {'organizations': request.user.orgs_admin.all()})

@login_required
def org_home(request, pk):
    o = get_object_or_404(Organization.objects, pk=pk)
    if not request.user == o.admin:
        messages.error("You aren't authorized to do that!")
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
        messages.error("That's not your organization!")
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
    if request.method == "GET":
        return render(request, 'main/org_new.html')
    else:
        o = Organization(admin=request.user)
        err = validate_org(request, o)
        if isinstance(err, tuple):
            return render(request, 'main/org_new.html', {'org': err[1], 'errors': err[0]})
        messages.success(request, 'Organization successfully created')
        return HttpResponseRedirect(reverse('main:manage_home'))

@login_required
def org_delete(request, pk):
    o = Organization.objects.get(pk=pk)
    if o:
        if request.user == o.admin:
            o.delete()
            messages.info(request, "Organization successfully deleted")
        else:
            messages.error(request, "You aren't authorized to do that!")
    else:
        messages.error(request, "Organization not found!")
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET.get('next'))
    return HttpResponseRedirect('/')
