# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Seat'
        db.delete_table(u'row_seat')

        # Deleting field 'Lineup.practice'
        db.delete_column(u'row_lineup', 'practice_id')


        # Changing field 'Lineup.piece'
        db.alter_column(u'row_lineup', 'piece_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['row.Piece']))
        # Adding M2M table for field athletes on 'Lineup'
        m2m_table_name = db.shorten_name(u'row_lineup_athletes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lineup', models.ForeignKey(orm[u'row.lineup'], null=False)),
            ('athlete', models.ForeignKey(orm[u'row.athlete'], null=False))
        ))
        db.create_unique(m2m_table_name, ['lineup_id', 'athlete_id'])


    def backwards(self, orm):
        # Adding model 'Seat'
        db.create_table(u'row_seat', (
            ('athlete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['row.Athlete'])),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lineup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['row.Lineup'])),
        ))
        db.send_create_signal(u'row', ['Seat'])

        # Adding field 'Lineup.practice'
        db.add_column(u'row_lineup', 'practice',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['row.Practice'], null=True),
                      keep_default=False)


        # Changing field 'Lineup.piece'
        db.alter_column(u'row_lineup', 'piece_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['row.Piece'], null=True))
        # Removing M2M table for field athletes on 'Lineup'
        db.delete_table(db.shorten_name(u'row_lineup_athletes'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'row.athlete': {
            'Meta': {'object_name': 'Athlete'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'side': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Active'", 'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'})
        },
        u'row.boat': {
            'Meta': {'object_name': 'Boat'},
            'coxed': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'seats': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'row.invite': {
            'Meta': {'object_name': 'Invite'},
            'canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'row.lineup': {
            'Meta': {'object_name': 'Lineup'},
            'athletes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['row.Athlete']", 'symmetrical': 'False'}),
            'boat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['row.Boat']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'piece': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['row.Piece']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'row.note': {
            'Meta': {'object_name': 'Note'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['row.Athlete']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'piece': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['row.Piece']", 'null': 'True'}),
            'practice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['row.Practice']", 'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'row.piece': {
            'Meta': {'object_name': 'Piece'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'practice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['row.Practice']"})
        },
        u'row.practice': {
            'Meta': {'object_name': 'Practice'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'workout': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'row.result': {
            'Meta': {'object_name': 'Result'},
            'athlete': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['row.Athlete']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'distance': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'piece': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['row.Piece']"}),
            'time': ('django.db.models.fields.IntegerField', [], {})
        },
        u'row.weight': {
            'Meta': {'object_name': 'Weight'},
            'athlete': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['row.Athlete']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '1'})
        }
    }

    complete_apps = ['row']