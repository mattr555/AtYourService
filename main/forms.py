from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from datetime import timedelta
from main.models import UserEvent, UserProfile, Organization, Event

import pytz

class MyUserCreate(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    volunteer = forms.BooleanField(required=False)
    org_admin = forms.BooleanField(required=False)
    timezone = forms.ChoiceField(required=True, choices=[(i, i) for i in pytz.common_timezones])

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'volunteer', 'org_admin', 'timezone',)
        model = User

    def save(self, commit=True):
        user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'],
                                        self.cleaned_data['password1'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data.get('volunteer'):
            user.groups.add(Group.objects.get(name="Volunteer"))
        if self.cleaned_data.get('org_admin'):
            user.groups.add(Group.objects.get(name="Org_Admin"))
        user.save()
        profile = UserProfile(user=user)
        profile.timezone = self.cleaned_data['timezone']
        profile.save()
        return user

    def clean_org_admin(self):
        vol = self.cleaned_data.get('volunteer')
        org = self.cleaned_data.get('org_admin')
        if (not vol) and (not org):
            raise forms.ValidationError('A checkbox is required')

class UserEventCreate(forms.ModelForm):
    date_start = forms.DateTimeField(required=True, widget=forms.DateTimeInput(format='%m/%d/%Y %I:%M %p'))
    date_end = forms.DateTimeField(widget=forms.DateTimeInput(format='%m/%d/%Y %I:%M %p'))

    class Meta:
        model = UserEvent
        fields = ('name', 'description', 'organization', 'date_start', 'date_end', 'location', 'hours_worked')

    def __init__(self, user=None, *args, **kwargs):
        super(UserEventCreate, self).__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        event = super(UserEventCreate, self).save(commit=False)
        event.user = self._user
        if self.cleaned_data.get('date_end') is None:
            event.date_end = event.date_start + timedelta(hours=event.hours_worked)
        if commit:
            event.save()
        return event

    def clean_date_end(self):
        date_end = self.cleaned_data.get('date_end')
        date_start = self.cleaned_data.get('date_start')
        if date_start > date_end:
            raise forms.ValidationError("The start date should be before the end date!")
        return date_end

class EventCreate(forms.ModelForm):
    date_start = forms.DateTimeField(required=True, widget=forms.DateTimeInput(format='%m/%d/%Y %I:%M %p'))
    date_end = forms.DateTimeField(widget=forms.DateTimeInput(format='%m/%d/%Y %I:%M %p'))

    class Meta:
        model = Event
        fields = ('organization', 'name', 'description', 'location', 'date_start', 'date_end', 'geo_lat', 'geo_lon',)

    def __init__(self, user=None, *args, **kwargs):
        super(EventCreate, self).__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        event = super(EventCreate, self).save(commit=False)
        event.user = self._user
        event.organizer_id = self.cleaned_data.get('organization').id
        if commit:
            event.save()
        return event

    def clean_organization(self):
        org = self.cleaned_data.get('organization')
        if org.admin_id != self._user.id:
            raise forms.ValidationError("That's not your organization!")
        return org

    def clean_date_end(self):
        date_end = self.cleaned_data.get('date_end')
        date_start = self.cleaned_data.get('date_start')
        if date_start > date_end:
            raise forms.ValidationError("The start date should be before the end date!")
        return date_end

class OrganizationCreate(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name', 'description', 'location', 'geo_lat', 'geo_lon')

    def __init__(self, user=None, *args, **kwargs):
        super(OrganizationCreate, self).__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        o = super(OrganizationCreate, self).save(commit=False)
        o.admin = self._user
        if commit:
            o.save()
        return o
