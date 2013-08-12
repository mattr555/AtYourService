from ajax.exceptions import AJAXError
from ajax.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from main.models import Event, Organization

@login_required
def do_event(request):
    event_id = int(request.POST.get('id'))
    vol = Group.objects.get(name='Volunteer')
    if event_id:
        if vol in request.user.groups.all():
            event = Event.objects.get(pk=event_id)
            event.participants.add(request.user)
            return {'user_status': event.status(request.user)}
        else:
            raise AJAXError(403, 'User must be a volunteer')

@login_required
def dont_do_event(request):
    event_id = int(request.POST.get('id'))
    if event_id:
        event = Event.objects.get(pk=event_id)
        event.participants.remove(request.user)
        return {'user_status': event.status(request.user)}

@login_required
def join_org(request):
    org_id = int(request.POST.get('id'))
    vol = Group.objects.get(name='Volunteer')
    if org_id:
        if vol in request.user.groups.all():
            org = Organization.objects.get(pk=org_id)
            org.members.add(request.user)
            return {}
        else:
            raise AJAXError(403, 'User must be a volunteer')

@login_required
def unjoin_org(request):
    org_id = int(request.POST.get('id'))
    if org_id:
        org = Organization.objects.get(pk=org_id)
        org.members.remove(request.user)
        return {}

