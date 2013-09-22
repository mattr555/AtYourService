from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from datetime import timedelta
from main.models import UserEvent, UserProfile

import pytz

class MyUserCreate(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    volunteer = forms.BooleanField(required=False)
    org_admin = forms.BooleanField(required=False)
    timezone = forms.ChoiceField(required=True)

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
    class Meta:
        model = UserEvent
        fields = ('name', 'description', 'date_start', 'date_end', 'location', 'hours_worked')

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
