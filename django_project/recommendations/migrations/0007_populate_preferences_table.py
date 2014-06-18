# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
import os


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'data/prefs.csv')

        data = open(filename, 'r')
        data = data.readlines()

        for line in data:
            listFromLine = line.split(',')

            user = listFromLine[0].decode('iso-8859-1').encode('utf8')
            movie_cid = listFromLine[1].decode('iso-8859-1').encode('utf8')
            rating = listFromLine[2].decode('iso-8859-1').encode('utf8')

            if orm.Movie.objects.filter(cid=movie_cid).exists():
                movie_obj = orm.Movie.objects.filter(cid=movie_cid)[0]

                p = orm.Preferences(user=user, movie=movie_obj, rating=rating)
                p.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'recommendations.movie': {
            'Meta': {'object_name': 'Movie'},
            'cid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'})
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
    symmetrical = True
