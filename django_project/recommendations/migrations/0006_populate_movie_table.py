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
        filename = os.path.join(dir, 'data/movies.csv')

        data = open(filename, 'r')
        data = data.readlines()

        forbidden_chars = ['|', '~', '{', '}']

        for line in data:
            listFromLine = line.split(',', 1)

            cid = listFromLine[0].decode('iso-8859-1').encode('utf8')
            name_list = listFromLine[1].decode('iso-8859-1').encode('utf8').split('\n')
            name = name_list[0]

            forbidden_chars_found = False
            for char in forbidden_chars:
                if char in name:
                    forbidden_chars_found = True
                    break;

            if forbidden_chars_found != True:
                m = orm.Movie(cid=cid, name=name)
                m.save()


    def backwards(self, orm):
        "Write your backwards methods here."

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
    symmetrical = True
