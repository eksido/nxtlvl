# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Deleting model 'ActionResponse'
        db.delete_table(u'mus_actionresponse')

        # Deleting model 'ActionKey'
        db.delete_table(u'mus_actionkey')

        # Deleting model 'ActionKeyToDevelopmentPlanRelation'
        db.delete_table(u'mus_actionkeytodevelopmentplanrelation')

        # Adding model 'ActionComment'
        db.create_table(u'mus_actioncomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_comment_created_by',
                                                                   to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_comment_updated_by',
                                                                   to=orm['auth.User'])),
        ))
        db.send_create_signal(u'mus', ['ActionComment'])

        # Deleting field 'Action.action_key'
        db.delete_column(u'mus_action', 'action_key_id')

        # Adding field 'Action.description'
        db.add_column(u'mus_action', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Action.my_effort'
        db.add_column(u'mus_action', 'my_effort',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Action.my_needs'
        db.add_column(u'mus_action', 'my_needs',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Action.approved_at'
        db.add_column(u'mus_action', 'approved_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Action.follow_up_at'
        db.add_column(u'mus_action', 'follow_up_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Action.status'
        db.add_column(u'mus_action', 'status',
                      self.gf('django.db.models.fields.IntegerField')(),
                      keep_default=False)

        # Adding field 'Action.employee'
        db.add_column(u'mus_action', 'employee',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.Employee']),
                      keep_default=False)


        # Changing field 'Action.title'
        db.alter_column(u'mus_action', 'title', self.gf('django.db.models.fields.TextField')(default=''))

    def backwards(self, orm):
        # Adding model 'ActionResponse'
        db.create_table(u'mus_actionresponse', (
            ('action_key_to_development_plan_relation',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_responses',
                                                                   to=orm['mus.ActionKeyToDevelopmentPlanRelation'])),
            ('updated_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_response_updated_by',
                                                                   to=orm['auth.User'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_responses',
                                                                             to=orm['mus.Action'])),
            ('text', self.gf('django.db.models.fields.TextField')(null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_response_created_by',
                                                                   to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'mus', ['ActionResponse'])

        # Adding model 'ActionKey'
        db.create_table(u'mus_actionkey', (
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_key_updated_by',
                                                                                 to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.TextField')(null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_key_created_by',
                                                                                 to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'mus', ['ActionKey'])

        # Adding model 'ActionKeyToDevelopmentPlanRelation'
        db.create_table(u'mus_actionkeytodevelopmentplanrelation', (
            ('action_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.ActionKey'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('development_plan_relation', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='action_key_to_development_plan_relation', to=orm['mus.DevelopmentPlan'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'mus', ['ActionKeyToDevelopmentPlanRelation'])

        # Deleting model 'ActionComment'
        db.delete_table(u'mus_actioncomment')

        # Adding field 'Action.action_key'
        db.add_column(u'mus_action', 'action_key',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions',
                                                                            to=orm['mus.ActionKey']),
                      keep_default=False)

        # Deleting field 'Action.description'
        db.delete_column(u'mus_action', 'description')

        # Deleting field 'Action.my_effort'
        db.delete_column(u'mus_action', 'my_effort')

        # Deleting field 'Action.my_needs'
        db.delete_column(u'mus_action', 'my_needs')

        # Deleting field 'Action.approved_at'
        db.delete_column(u'mus_action', 'approved_at')

        # Deleting field 'Action.follow_up_at'
        db.delete_column(u'mus_action', 'follow_up_at')

        # Deleting field 'Action.status'
        db.delete_column(u'mus_action', 'status')

        # Deleting field 'Action.employee'
        db.delete_column(u'mus_action', 'employee_id')


        # Changing field 'Action.title'
        db.alter_column(u'mus_action', 'title', self.gf('django.db.models.fields.TextField')(null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
                     'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
                'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                        'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                                  'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mus.action': {
            'Meta': {'object_name': 'Action'},
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'action_created_by'", 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Employee']"}),
            'follow_up_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'my_effort': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'my_needs': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'action_updated_by'", 'to': u"orm['auth.User']"})
        },
        u'mus.actioncomment': {
            'Meta': {'object_name': 'ActionComment'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'action_comment_created_by'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'action_comment_updated_by'", 'to': u"orm['auth.User']"})
        },
        u'mus.company': {
            'Meta': {'object_name': 'Company'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'company_created_by'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'company_updated_by'", 'to': u"orm['auth.User']"})
        },
        u'mus.competence': {
            'Meta': {'object_name': 'Competence'},
            'competence_field': ('django.db.models.fields.related.ForeignKey', [],
                                 {'related_name': "'competence_competence_field'",
                                  'to': u"orm['mus.CompetenceField']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_created_by'", 'to': u"orm['auth.User']"}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_updated_by'", 'to': u"orm['auth.User']"})
        },
        u'mus.competencefield': {
            'Meta': {'object_name': 'CompetenceField'},
            'company': ('django.db.models.fields.related.ForeignKey', [],
                        {'default': 'None', 'to': u"orm['mus.Company']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_field_created_by'", 'to': u"orm['auth.User']"}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_field_updated_by'", 'to': u"orm['auth.User']"})
        },
        u'mus.developmentplan': {
            'Meta': {'object_name': 'DevelopmentPlan'},
            'competence_fields': ('django.db.models.fields.related.ManyToManyField', [],
                                  {'related_name': "'development_plan_competence_fields'", 'symmetrical': 'False',
                                   'to': u"orm['mus.CompetenceField']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'development_plan_created_by'", 'to': u"orm['auth.User']"}),
            'employee_response_relation': ('django.db.models.fields.related.ForeignKey', [],
                                           {'related_name': "'development_plan_employee'",
                                            'to': u"orm['mus.DevelopmentPlanToUserRelation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager_response_relation': ('django.db.models.fields.related.ForeignKey', [],
                                          {'related_name': "'development_plan_manager'",
                                           'to': u"orm['mus.DevelopmentPlanToUserRelation']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Employee']"})
        },
        u'mus.developmentplantouserrelation': {
            'Meta': {'object_name': 'DevelopmentPlanToUserRelation'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'development_plan_user_created_by'", 'to': u"orm['auth.User']"}),
            'finished_at': (
                'django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'mus.employee': {
            'Meta': {'object_name': 'Employee'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Company']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'employee_created_by'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': u"orm['mus.Employee']", 'null': 'True', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [],
                      {'to': u"orm['mus.Role']", 'through': u"orm['mus.EmployeeRole']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'employee_updated_by'", 'to': u"orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [],
                     {'related_name': "'employee_user'", 'to': u"orm['auth.User']"})
        },
        u'mus.employeerole': {
            'Meta': {'object_name': 'EmployeeRole'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'employee_role_created_by'", 'to': u"orm['auth.User']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Role']"})
        },
        u'mus.file': {
            'Meta': {'object_name': 'File'},
            'company': (
                'django.db.models.fields.related.ForeignKey', [],
                {'related_name': "'files'", 'to': u"orm['mus.Company']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'file_created_by'", 'to': u"orm['auth.User']"}),
            'file': ('django.db.models.fields.related.ForeignKey', [],
                     {'default': 'None', 'to': u"orm['mus.FileBytes']", 'null': 'True', 'blank': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_size': ('django.db.models.fields.BigIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'role': ('django.db.models.fields.related.ForeignKey', [],
                     {'default': 'None', 'related_name': "'files'", 'null': 'True', 'blank': 'True',
                      'to': u"orm['mus.Role']"})
        },
        u'mus.filebytes': {
            'Meta': {'object_name': 'FileBytes'},
            '_data': ('django.db.models.fields.TextField', [], {'db_column': "'data'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'mus.question': {
            'Meta': {'object_name': 'Question'},
            'competence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Competence']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'question_created_by'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('tinymce.models.HTMLField', [], {'max_length': '4000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'question_updated_by'", 'to': u"orm['auth.User']"})
        },
        u'mus.questionresponse': {
            'Meta': {'object_name': 'QuestionResponse'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'question_response_created_by'", 'to': u"orm['auth.User']"}),
            'development_plan_to_user_relation': ('django.db.models.fields.related.ForeignKey', [], {
                'related_name': "'question_response_development_plan_to_user_relation'",
                'to': u"orm['mus.DevelopmentPlanToUserRelation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Question']"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'question_response_updated_by'", 'to': u"orm['auth.User']"})
        },
        u'mus.role': {
            'Meta': {'object_name': 'Role'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'role_created_by'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'role_updated_by'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['mus']