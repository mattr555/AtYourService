from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.cache import cache
from geopy import geocoders

from math import sin, cos, acos, radians

def distance(p1_lat, p1_long, p2_lat, p2_long):
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

from django.dispatch import receiver
from django.db.backends.signals import connection_created

@receiver(connection_created)
def setup_proximity_func(connection, **kwargs):
    # add the proximity function to sqlite
    connection.connection.create_function("distance", 4, distance)

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

    admin = models.ForeignKey(User, related_name='orgs_admin')
    members = models.ManyToManyField(User, related_name='organizations')
    name = models.CharField(max_length=300, db_index=True)
    description = models.TextField()
    location = models.CharField(max_length=200)
    geo_lat = models.FloatField(blank=True, null=True)
    geo_lon = models.FloatField(blank=True, null=True)

class EventManager(models.Manager):
    def within(self, location, distance):
        subquery = 'distance(%(geo_lat)s,%(geo_lon)s,main_event.geo_lat,main_event.geo_lon) ' % location.__dict__
        condition = 'proximity < %s' % distance
        order = 'date_end'
        query = self.extra(select={'proximity':subquery},
                          where=[condition], order_by=[order])
        return query

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
        result = cache.get('user_' + self.id + '_org_admin')
        if result is None:
            group = Group.objects.get(name="Org_Admin")
            result = group in self.user.groups.all()
            cache.set('user_' + self.id + '_org_admin', result)
        return result

    def is_volunteer(self):
        result = cache.get('user_' + self.id + '_volunteer')
        if result is None:
            group = Group.objects.get(name="Volunteer")
            result = group in self.user.groups.all()
            cache.set('user_' + self.id + '_volunteer', result)
        return result

    user = models.OneToOneField(User, unique=True, related_name='user_profile')
    geo_lat = models.FloatField(blank=True, null=True)
    geo_lon = models.FloatField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
