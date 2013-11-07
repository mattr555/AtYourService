from django.contrib import admin
from main.models import Event, Organization

class EventInline(admin.StackedInline):
	model = Event
	fieldsets = [
		(None, {'fields': ['name', 'description', 'date_start', 'date_end', 'organizer']}),
		('Participants', {'fields': ['participants', 'confirmed_participants'], 'classes': ['collapse']})
	]
	filter_horizontal = ['participants', 'confirmed_participants']
	extra = 1

class OrganizationAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name', 'description', 'location']}),
		('Members', {'fields': ['members'], 'classes': ['collapse']})
	]
	list_display = ('name', 'admin', 'location', 'member_count', 'event_count')
	search_fields = ['name']
	filter_horizontal = ['members']
	inlines = [EventInline]


admin.site.register(Organization, OrganizationAdmin)
