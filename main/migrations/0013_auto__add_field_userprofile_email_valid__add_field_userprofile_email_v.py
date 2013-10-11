# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.email_valid'
        db.add_column('main_userprofile', 'email_valid',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.email_validation_key'
        db.add_column('main_userprofile', 'email_validation_key',
                      self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=50),
                      keep_default=False)


        # Changing field 'UserProfile.location'
        db.alter_column('main_userprofile', 'location', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'UserProfile.timezone'
        db.alter_column('main_userprofile', 'timezone', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

    def backwards(self, orm):
        # Deleting field 'UserProfile.email_valid'
        db.delete_column('main_userprofile', 'email_valid')

        # Deleting field 'UserProfile.email_validation_key'
        db.delete_column('main_userprofile', 'email_validation_key')


        # Changing field 'UserProfile.location'
        db.alter_column('main_userprofile', 'location', self.gf('django.db.models.fields.CharField')(null=True, max_length=100))

        # Changing field 'UserProfile.timezone'
        db.alter_column('main_userprofile', 'timezone', self.gf('django.db.models.fields.CharField')(null=True, max_length=100))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.event': {
            'Meta': {'object_name': 'Event'},
            'confirmed_participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'confirmed_events'", 'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['main.Organization']"}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events_organized'", 'to': "orm['auth.User']"}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'events'", 'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'main.organization': {
            'Meta': {'object_name': 'Organization'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orgs_admin'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'organizations'", 'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300'})
        },
        'main.userevent': {
            'Meta': {'object_name': 'UserEvent'},
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hours_worked': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_events'", 'to': "orm['auth.User']"})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_validation_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'timezone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['main']