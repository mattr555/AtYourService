from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

@login_required
def org_manage(request):
    if not request.user.user_profile.is_org_admin:
        messages.error("You aren't an administrator of an organization!")
        return HttpResponseRedirect('/')
    return render(request, 'main/org_home.html', {'organizations': request.user.orgs_admin.all()})
