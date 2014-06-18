# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        queryset = orm.Preferences.objects.all()
        for obj in queryset:
            user = obj.user
            movie = obj.movie
            rating = obj.rating
            pref_obj = orm.Preferences_2(user=user, movie=movie,rating=rating)
            pref_obj.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'recommendations.movie': {
            'Meta': {'object_name': 'Movie'},
            'cid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {}),
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
        },
        u'recommendations.preferences_2': {
            'Meta': {'object_name': 'Preferences_2'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recommendations.Movie']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.IntegerField', [], {})
        },
        u'recommendations.userrelations': {
            'Meta': {'object_name': 'UserRelations'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'similarity_coeff': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '5', 'blank': 'True'}),
            'user_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['recommendations']
    symmetrical = True
