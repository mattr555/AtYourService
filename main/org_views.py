from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from main.models import Organization

@login_required
def org_manage(request):
    if not request.user.user_profile.is_org_admin:
        messages.error("You aren't an organization administrator!")
        return HttpResponseRedirect('/')
    return render(request, 'main/org_home.html', {'organizations': request.user.orgs_admin.all()})

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
            return render(request, 'main.org_edit.html', {'org': err[1], 'errors': err[0]})
        messages.success(request, 'Organization successfully edited')
        return HttpResponseRedirect(reverse('main:org_manage'))

