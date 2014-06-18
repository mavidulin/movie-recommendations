# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Movie.view_counter'
        db.add_column(u'recommendations_movie', 'view_counter',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Movie.view_counter'
        db.delete_column(u'recommendations_movie', 'view_counter')


    models = {
        u'recommendations.movie': {
            'Meta': {'object_name': 'Movie'},
            'cid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'view_counter': ('django.db.models.fields.IntegerField', [], {})
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