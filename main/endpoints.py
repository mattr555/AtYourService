from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from main.models import Event, Organization
import json
from decorator import decorator

def JsonResponse(data):
    resp = json.dumps({'success': True, 'data': data})
    return HttpResponse(resp, mimetype='application/json')

def NotFound(msg):
    error = {
            'success': False,
            'data': {
                'code': 404,
                'message': msg
            }
        }
    resp = HttpResponseNotFound()
    resp.content = json.dumps(error)
    return resp

def Forbidden(msg):
    error = {
            'success': False,
            'data': {
                'code': 403,
                'message': msg
            }
        }
    resp = HttpResponseForbidden()
    resp.content = json.dumps(error)
    return resp

@decorator
def login_required(f, *args, **kwargs):
    if not args[0].user.is_authenticated:
        raise Forbidden('User is not logged in')
    return f(*args, **kwargs)

@login_required
def do_event(request):
    event_id = int(request.POST.get('id'))
    vol = Group.objects.get(name='Volunteer')
    if event_id:
        if vol in request.user.groups.all():
            event = Event.objects.get(pk=event_id)
            event.participants.add(request.user)
            data = {'user_status': event.status(request.user)}
            return JsonResponse(data)
        else:
            raise Forbidden('User must be a volunteer')

@login_required
def dont_do_event(request):
    event_id = int(request.POST.get('id'))
    if event_id:
        event = Event.objects.get(pk=event_id)
        event.participants.remove(request.user)
        return JsonResponse({'user_status': event.status(request.user)})

@login_required
def join_org(request):
    org_id = int(request.POST.get('id'))
    vol = Group.objects.get(name='Volunteer')
    if org_id:
        if vol in request.user.groups.all():
            org = Organization.objects.get(pk=org_id)
            org.members.add(request.user)
            return JsonResponse({})
        else:
            raise Forbidden('User must be a volunteer')

@login_required
def unjoin_org(request):
    org_id = int(request.POST.get('id'))
    if org_id:
        org = Organization.objects.get(pk=org_id)
        org.members.remove(request.user)
        return JsonResponse({})

@login_required
def confirm_participant(request):
    e = Event.objects.get(id=int(request.POST.get('event_id')))
    if not e:
        raise NotFound("Event not found")
    if request.user.id == e.organizer_id:
        u = User.objects.get(id=int(request.POST.get('user_id')))
        if not u:
            raise NotFound("User not found")
        if u in e.participants.all():
            e.confirmed_participants.add(u)
        else:
            raise NotFound("User is not a participant")
        status = e.confirm_status(u)
        return JsonResponse({'status': status.status,
                'row_class': status.row_class,
                'button_class': status.button_class,
                'button_text': status.button_text})
    else:
        raise Forbidden("User must be event organizer")

@login_required
def unconfirm_participant(request):
    e = Event.objects.get(id=int(request.POST.get('event_id')))
    if not e:
        raise NotFound("Event not found")
    if request.user.id == e.organizer_id:
        u = User.objects.get(id=int(request.POST.get('user_id')))
        if not u:
            raise NotFound("User not found")
        if u in e.participants.all() and u in e.confirmed_participants.all():
            e.confirmed_participants.remove(u)
        else:
            raise NotFound("User is not a participant")
        status = e.confirm_status(u)
        return JsonResponse({'status': status.status,
                'row_class': status.row_class,
                'button_class': status.button_class,
                'button_text': status.button_text})
    else:
        raise Forbidden("User must be event organizer")

def username_valid(request):
    if request.POST.get('username', ''):
        try:
            u = User.objects.get(username=request.POST.get('username'))
            return JsonResponse({'message': 'This username is in use', 'valid': False})
        except User.DoesNotExist:
            return JsonResponse({'message': 'This username is valid', 'valid': True})
    return JsonResponse({'message': 'Please enter a value', 'valid': False})
