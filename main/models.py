from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.core.urlresolvers import reverse

from geopy import geocoders
from collections import namedtuple
from math import sin, cos, acos, radians
import datetime

ConfirmTuple = namedtuple('ConfirmTuple', 'status row_class button_class button_text')

def haversin(p1_lat, p1_long, p2_lat, p2_long):
        # calculates the distance between p1 and p2
        multiplier = 3959  # for miles
        if p1_lat and p1_long and p2_lat and p2_long:
            return (multiplier *
                acos(
                    cos(radians(p1_lat)) *
                    cos(radians(p2_lat)) *
                    cos(radians(p2_long) - radians(p1_long)) +
                    sin(radians(p1_lat)) * sin(radians(p2_lat))
                )
            )

class Organization(models.Model):
    def __str__(self):
        return self.name

    def detail_url(self):
        return reverse('main:organization_detail', args=(self.pk,))

    def populate_geo(self):
        geo = geocoders.GoogleV3()
        try:
            place, (lat, lon) = geo.geocode(self.location)
            self.geo_lat = lat
            self.geo_lon = lon
        except:
            pass

    def member_count(self):
        return self.members.count()

    def event_count(self):
        return self.events.count()

    admin = models.ForeignKey(User, related_name='orgs_admin')
    members = models.ManyToManyField(User, related_name='organizations')
    name = models.CharField(max_length=300, db_index=True)
    description = models.TextField()
    location = models.CharField(max_length=200)
    geo_lat = models.FloatField(blank=True, null=True)
    geo_lon = models.FloatField(blank=True, null=True)

class EventManager(models.Manager):
    def within(self, location, distance, upcoming=True):
        loc_lat, loc_lon = location.geo_lat, location.geo_lon
        lat_upper = loc_lat + (distance / 69)
        lat_lower = loc_lat - (distance / 69)
        lon_upper = loc_lon + (distance / 69)
        lon_lower = loc_lon - (distance / 69)
        set = self.filter(geo_lat__lt=lat_upper,
                          geo_lat__gt=lat_lower,
                          geo_lon__lt=lon_upper,
                          geo_lon__gt=lon_lower)
        if upcoming:
            set = set.filter(date_end__gt=timezone.now())
        exclude_list = []
        for i in set.all():
            if haversin(loc_lat, loc_lon, i.geo_lat, i.geo_lon) > distance:
                exclude_list.append(i.id)
        set = set.exclude(id__in=exclude_list)
        return set

class Event(models.Model):
    def __str__(self):
        return self.name

    def hours(self):
        delta = self.date_end - self.date_start
        return round((delta.seconds / 60 / 60) + (delta.days * 24), 2)

    def detail_url(self):
        return reverse('main:event_detail', args=(self.pk,))

    def status(self, user):
        if user == self.organizer:
            return "Organizing"
        if user in self.participants.all():
            if timezone.now() < self.date_start:
                return "Event has not occurred yet"
            elif user in self.confirmed_participants.all():
                return "Confirmed"
            else:
                return "Unconfirmed"
        return "Not participating"

    def confirm_status(self, user):
        ROW_CLASSES = {"Unconfirmed": "warning",
                       "Confirmed": "success"}
        BUTTON_CLASSES = {"Unconfirmed": "btn-success",
                          "Confirmed": "btn-warning"}
        BUTTON_TEXT = {"Unconfirmed": "Confirm",
                       "Confirmed": "Unconfirm"}
        status = self.status(user)
        return ConfirmTuple(status,
                            ROW_CLASSES.get(status, ""),
                            BUTTON_CLASSES.get(status, ""),
                            BUTTON_TEXT.get(status, ""))

    def row_class(self, user):
        ROW_CLASSES = {"Unconfirmed": "warning",
                       "Confirmed": "success"}
        return ROW_CLASSES.get(self.status(user), "")

    def getOrganization(self):
        return self.organization.name

    def populate_geo(self):
        geo = geocoders.GoogleV3()
        try:
            place, (lat, lon) = geo.geocode(self.location)
            self.geo_lat = lat
            self.geo_lon = lon
        except:
            pass

    def participant_count(self):
        return self.participants.all().count()

    def date_start_input(self):
        return datetime.datetime.strftime(self.date_start, '%m/%d/%y %I:%M %p')

    def date_end_input(self):
        return datetime.datetime.strftime(self.date_end, '%m/%d/%y %I:%M %p')

    has_org_url = True
    objects = EventManager()

    participants = models.ManyToManyField(User, related_name='events')
    confirmed_participants = models.ManyToManyField(User, related_name='confirmed_events')
    organizer = models.ForeignKey(User, related_name='events_organized')
    organization = models.ForeignKey(Organization, related_name='events')
    name = models.CharField(max_length=300, db_index=True)
    description = models.TextField()
    date_start = models.DateTimeField(db_index=True)
    date_end = models.DateTimeField(db_index=True)
    location = models.CharField(max_length=100)
    geo_lat = models.FloatField(blank=True, null=True)
    geo_lon = models.FloatField(blank=True, null=True)

class UserEvent(models.Model):
    def __str__(self):
        return self.name

    def hours(self):
        return self.hours_worked

    def detail_url(self):
        return reverse('main:userevent_detail', args=(self.pk,))

    def status(self, user):
        if user == self.user:
            if timezone.now() < self.date_start:
                return "Event has not occurred yet"
            return "User-created Event"
        return "Not participating"

    def row_class(self, user):
        return "success" if self.status(user) == "User-created Event" else ""

    def getOrganization(self):
        return self.organization

    def populate_geo(self):
        geo = geocoders.GoogleV3()
        try:
            place, (lat, lon) = geo.geocode(self.location)
            self.geo_lat = lat
            self.geo_lon = lon
        except:
            pass

    has_org_url = False
    user = models.ForeignKey(User, related_name='user_events')
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField(blank=True, null=True, db_index=True)
    location = models.CharField(max_length=100)
    geo_lat = models.FloatField(blank=True, null=True)
    geo_lon = models.FloatField(blank=True, null=True)
    hours_worked = models.FloatField('hours worked')

class UserProfile(models.Model):
    def __str__(self):
        return self.user.get_full_name()

    def populate_geo(self):
        geo = geocoders.GoogleV3()
        try:
            place, (lat, lon) = geo.geocode(self.location)
            self.geo_lat = lat
            self.geo_lon = lon
        except:
            pass

    def is_org_admin(self):
        return self.user.has_perm('main.add_organization')
        
    def is_volunteer(self):
        return self.user.has_perm('main.add_userevent')

    user = models.OneToOneField(User, unique=True, related_name='user_profile')
    geo_lat = models.FloatField(blank=True, null=True)
    geo_lon = models.FloatField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=100, blank=True)
    email_valid = models.BooleanField(default=False)
    email_validation_key = models.CharField(max_length=50, blank=True)
