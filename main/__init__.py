from django.contrib.auth.models import Permission, Group
from south.signals import post_migrate

def add_groups(sender, **kwargs):
	group, created = Group.objects.get_or_create(name='Volunteer')
	if created:
		p = Permission.objects.get(codename='add_userevent')
		group.permissions.add(p)
	group, created = Group.objects.get_or_create(name='Org_Admin')
	if created:
		p = Permission.objects.get(codename='add_organization')
		group.permissions.add(p)

post_migrate.connect(add_groups)
