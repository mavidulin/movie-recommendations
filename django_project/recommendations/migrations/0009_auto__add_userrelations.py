# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserRelations'
        db.create_table(u'recommendations_userrelations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user_2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('similarity_coeff', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=5, blank=True)),
        ))
        db.send_create_signal(u'recommendations', ['UserRelations'])


    def backwards(self, orm):
        # Deleting model 'UserRelations'
        db.delete_table(u'recommendations_userrelations')


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