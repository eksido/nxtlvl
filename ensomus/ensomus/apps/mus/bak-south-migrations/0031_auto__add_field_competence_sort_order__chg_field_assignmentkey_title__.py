# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding field 'Competence.sort_order'
        db.add_column('mus_competence', 'sort_order',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


        # Changing field 'AssignmentKey.title'
        db.alter_column('mus_assignmentkey', 'title', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Assignment.title'
        db.alter_column('mus_assignment', 'title', self.gf('tinymce.models.HTMLField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Competence.sort_order'
        db.delete_column('mus_competence', 'sort_order')


        # User chose to not deal with backwards NULL issues for 'AssignmentKey.title'
        raise RuntimeError("Cannot reverse this migration. 'AssignmentKey.title' and its values cannot be restored.")

        # Changing field 'Assignment.title'
        db.alter_column('mus_assignment', 'title', self.gf('django.db.models.fields.TextField')(null=True))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')",
                     'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
                'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mus.action': {
            'Meta': {'object_name': 'Action'},
            'action_key': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'actions'", 'to': "orm['mus.ActionKey']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'action_created_by'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'action_updated_by'", 'to': "orm['auth.User']"})
        },
        'mus.actionkey': {
            'Meta': {'object_name': 'ActionKey'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'action_key_created_by'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'action_key_updated_by'", 'to': "orm['auth.User']"})
        },
        'mus.actionkeytodevelopmentplanrelation': {
            'Meta': {'object_name': 'ActionKeyToDevelopmentPlanRelation'},
            'action_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.ActionKey']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'development_plan_relation': ('django.db.models.fields.related.ForeignKey', [],
                                          {'related_name': "'action_key_to_development_plan_relation'",
                                           'to': "orm['mus.DevelopmentPlan']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'mus.actionresponse': {
            'Meta': {'object_name': 'ActionResponse'},
            'action': ('django.db.models.fields.related.ForeignKey', [],
                       {'related_name': "'action_responses'", 'to': "orm['mus.Action']"}),
            'action_key_to_development_plan_relation': ('django.db.models.fields.related.ForeignKey', [],
                                                        {'related_name': "'action_responses'",
                                                         'to': "orm['mus.ActionKeyToDevelopmentPlanRelation']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'action_response_created_by'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'action_response_updated_by'", 'to': "orm['auth.User']"})
        },
        'mus.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'assignment_key': ('django.db.models.fields.related.ForeignKey', [],
                               {'related_name': "'assignments'", 'to': "orm['mus.AssignmentKey']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'assignment_created_by'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('tinymce.models.HTMLField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'assignment_updated_by'", 'to': "orm['auth.User']"})
        },
        'mus.assignmentkey': {
            'Meta': {'object_name': 'AssignmentKey'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'mus.assignmentkeytouserrelation': {
            'Meta': {'object_name': 'AssignmentKeyToUserRelation'},
            'assignment_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.AssignmentKey']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'assignment_key_to_user_relation_created_by'", 'to': "orm['auth.User']"}),
            'finished_at': (
                'django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mus.assignmentresponse': {
            'Meta': {'object_name': 'AssignmentResponse'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'assignment_responses'", 'to': "orm['mus.Assignment']"}),
            'assignment_key_to_user_relation': ('django.db.models.fields.related.ForeignKey', [],
                                                {'related_name': "'assignment_responses'",
                                                 'to': "orm['mus.AssignmentKeyToUserRelation']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text_assignment': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'text_competence': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'mus.company': {
            'Meta': {'object_name': 'Company'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'company_created_by'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'company_updated_by'", 'to': "orm['auth.User']"})
        },
        'mus.competence': {
            'Meta': {'object_name': 'Competence'},
            'competence_field': ('django.db.models.fields.related.ForeignKey', [],
                                 {'related_name': "'competence_competence_field'", 'to': "orm['mus.CompetenceField']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_created_by'", 'to': "orm['auth.User']"}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_updated_by'", 'to': "orm['auth.User']"})
        },
        'mus.competencefield': {
            'Meta': {'object_name': 'CompetenceField'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_field_created_by'", 'to': "orm['auth.User']"}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [],
                          {'to': "orm['mus.Question']", 'through': "orm['mus.CompetenceQuestion']",
                           'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_field_updated_by'", 'to': "orm['auth.User']"})
        },
        'mus.competencefieldcollection': {
            'Meta': {'object_name': 'CompetenceFieldCollection'},
            'competence_fields': ('django.db.models.fields.related.ManyToManyField', [],
                                  {'related_name': "'competence_field_collection_competence_fields'",
                                   'symmetrical': 'False',
                                   'through': "orm['mus.CompetenceFieldCollectionCompetenceField']",
                                   'to': "orm['mus.CompetenceField']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_field_collection_created_by'", 'to': "orm['auth.User']"}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_field_collection_updated_by'", 'to': "orm['auth.User']"})
        },
        'mus.competencefieldcollectioncompetencefield': {
            'Meta': {'object_name': 'CompetenceFieldCollectionCompetenceField'},
            'competence_field': (
                'django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.CompetenceField']"}),
            'competence_field_collection': (
                'django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.CompetenceFieldCollection']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_field_collection_competence_field_created_by'",
                            'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {})
        },
        'mus.competencefieldcollectiontocompanyrelation': {
            'Meta': {'object_name': 'CompetenceFieldCollectionToCompanyRelation'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.Company']"}),
            'competence_field_collection': (
                'django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.CompetenceFieldCollection']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_field_collection_company_created_by'",
                            'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mus.competencefieldcollectiontouserrelation': {
            'Meta': {'object_name': 'CompetenceFieldCollectionToUserRelation'},
            'competence_field_collection': ('django.db.models.fields.related.ForeignKey', [],
                                            {'related_name': "'parent'", 'to': "orm['mus.CompetenceFieldCollection']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_field_collection_user_created_by'", 'to': "orm['auth.User']"}),
            'finished_at': (
                'django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mus.competencequestion': {
            'Meta': {'object_name': 'CompetenceQuestion'},
            'competence_field': (
                'django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.CompetenceField']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'competence_question_created_by'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.Question']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {})
        },
        'mus.developmentplan': {
            'Meta': {'object_name': 'DevelopmentPlan'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'development_plan_created_by'", 'to': "orm['auth.User']"}),
            'employee_assignment_key_relation': ('django.db.models.fields.related.ForeignKey', [],
                                                 {'related_name': "'development_plan_employee_assignment_key_relation'",
                                                  'to': "orm['mus.AssignmentKeyToUserRelation']"}),
            'employee_response_relation': ('django.db.models.fields.related.ForeignKey', [],
                                           {'related_name': "'development_plan_employee'",
                                            'to': "orm['mus.CompetenceFieldCollectionToUserRelation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager_assignment_key_relation': ('django.db.models.fields.related.ForeignKey', [],
                                                {'related_name': "'development_plan_manager_assignment_key_relation'",
                                                 'to': "orm['mus.AssignmentKeyToUserRelation']"}),
            'manager_response_relation': ('django.db.models.fields.related.ForeignKey', [],
                                          {'related_name': "'development_plan_manager'",
                                           'to': "orm['mus.CompetenceFieldCollectionToUserRelation']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.Employee']"})
        },
        'mus.employee': {
            'Meta': {'object_name': 'Employee'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.Company']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'employee_created_by'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': "orm['mus.Employee']", 'null': 'True', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [],
                      {'to': "orm['mus.Role']", 'through': "orm['mus.EmployeeRole']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'employee_updated_by'", 'to': "orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [],
                     {'related_name': "'employee_user'", 'to': "orm['auth.User']"})
        },
        'mus.employeerole': {
            'Meta': {'object_name': 'EmployeeRole'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'employee_role_created_by'", 'to': "orm['auth.User']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.Role']"})
        },
        'mus.file': {
            'Meta': {'object_name': 'File'},
            'company': (
                'django.db.models.fields.related.ForeignKey', [],
                {'related_name': "'files'", 'to': "orm['mus.Company']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'file_created_by'", 'to': "orm['auth.User']"}),
            'file': ('django.db.models.fields.related.ForeignKey', [],
                     {'default': 'None', 'to': "orm['mus.FileBytes']", 'null': 'True', 'blank': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_size': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'role': ('django.db.models.fields.related.ForeignKey', [],
                     {'default': 'None', 'related_name': "'files'", 'null': 'True', 'blank': 'True',
                      'to': "orm['mus.Role']"})
        },
        'mus.filebytes': {
            'Meta': {'object_name': 'FileBytes'},
            '_data': ('django.db.models.fields.TextField', [], {'db_column': "'data'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mus.question': {
            'Meta': {'object_name': 'Question'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'question_created_by'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('tinymce.models.HTMLField', [], {'max_length': '4000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'question_updated_by'", 'to': "orm['auth.User']"})
        },
        'mus.questionresponse': {
            'Meta': {'object_name': 'QuestionResponse'},
            'competence_field_collection_to_user_relation': ('django.db.models.fields.related.ForeignKey', [], {
                'related_name': "'question_response_competence_field_collection_to_user_relation'",
                'to': "orm['mus.CompetenceFieldCollectionToUserRelation']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'question_response_created_by'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mus.Question']"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'question_response_updated_by'", 'to': "orm['auth.User']"})
        },
        'mus.role': {
            'Meta': {'object_name': 'Role'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'role_created_by'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'role_updated_by'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['mus']