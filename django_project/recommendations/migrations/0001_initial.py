# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Movie'
        db.create_table(u'recommendations_movie', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cid', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
        ))
        db.send_create_signal(u'recommendations', ['Movie'])

        # Adding model 'Preferences'
        db.create_table(u'recommendations_preferences', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.IntegerField')()),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recommendations.Movie'])),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'recommendations', ['Preferences'])

        # Adding model 'MovieRecom'
        db.create_table(u'recommendations_movierecom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.IntegerField')()),
            ('movie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recommendations.Movie'])),
        ))
        db.send_create_signal(u'recommendations', ['MovieRecom'])


    def backwards(self, orm):
        # Deleting model 'Movie'
        db.delete_table(u'recommendations_movie')

        # Deleting model 'Preferences'
        db.delete_table(u'recommendations_preferences')

        # Deleting model 'MovieRecom'
        db.delete_table(u'recommendations_movierecom')


    models = {
        u'recommendations.movie': {
            'Meta': {'object_name': 'Movie'},
            'cid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'})
        },
        u'recommendations.movierecom': {
            'Meta': {'object_name': 'MovieRecom'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recommendations.Movie']"}),
            'user': ('django.db.models.fields.IntegerField', [], {})
        },
        u'recommendations.preferences': {
            'Meta': {'object_name': 'Preferences'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recommendations.Movie']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['recommendations']