# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Question.updated_by'
        db.alter_column(u'mus_question', 'updated_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'Question.created_by'
        db.alter_column(u'mus_question', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'Competence.created_by'
        db.alter_column(u'mus_competence', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'Competence.updated_by'
        db.alter_column(u'mus_competence', 'updated_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'Company.created_by'
        db.alter_column(u'mus_company', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'Company.updated_by'
        db.alter_column(u'mus_company', 'updated_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'Action.created_by'
        db.alter_column(u'mus_action', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'Action.updated_by'
        db.alter_column(u'mus_action', 'updated_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'QuestionResponse.updated_by'
        db.alter_column(u'mus_questionresponse', 'updated_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'QuestionResponse.created_by'
        db.alter_column(u'mus_questionresponse', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'DevelopmentPlan.created_by'
        db.alter_column(u'mus_developmentplan', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'ActionComment.updated_by'
        db.alter_column(u'mus_actioncomment', 'updated_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'ActionComment.created_by'
        db.alter_column(u'mus_actioncomment', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'CompetenceField.created_by'
        db.alter_column(u'mus_competencefield', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'CompetenceField.updated_by'
        db.alter_column(u'mus_competencefield', 'updated_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'DevelopmentPlanToUserRelation.created_by'
        db.alter_column(u'mus_developmentplantouserrelation', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'EmployeeRole.created_by'
        db.alter_column(u'mus_employeerole', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'File.created_by'
        db.alter_column(u'mus_file', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'Employee.updated_by'
        db.alter_column(u'mus_employee', 'updated_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'Employee.created_by'
        db.alter_column(u'mus_employee', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'Role.created_by'
        db.alter_column(u'mus_role', 'created_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

        # Changing field 'Role.updated_by'
        db.alter_column(u'mus_role', 'updated_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['auth.User']))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Question.updated_by'
        raise RuntimeError("Cannot reverse this migration. 'Question.updated_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Question.created_by'
        raise RuntimeError("Cannot reverse this migration. 'Question.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Competence.created_by'
        raise RuntimeError("Cannot reverse this migration. 'Competence.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Competence.updated_by'
        raise RuntimeError("Cannot reverse this migration. 'Competence.updated_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Company.created_by'
        raise RuntimeError("Cannot reverse this migration. 'Company.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Company.updated_by'
        raise RuntimeError("Cannot reverse this migration. 'Company.updated_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Action.created_by'
        raise RuntimeError("Cannot reverse this migration. 'Action.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Action.updated_by'
        raise RuntimeError("Cannot reverse this migration. 'Action.updated_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'QuestionResponse.updated_by'
        raise RuntimeError("Cannot reverse this migration. 'QuestionResponse.updated_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'QuestionResponse.created_by'
        raise RuntimeError("Cannot reverse this migration. 'QuestionResponse.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'DevelopmentPlan.created_by'
        raise RuntimeError("Cannot reverse this migration. 'DevelopmentPlan.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ActionComment.updated_by'
        raise RuntimeError("Cannot reverse this migration. 'ActionComment.updated_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ActionComment.created_by'
        raise RuntimeError("Cannot reverse this migration. 'ActionComment.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'CompetenceField.created_by'
        raise RuntimeError("Cannot reverse this migration. 'CompetenceField.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'CompetenceField.updated_by'
        raise RuntimeError("Cannot reverse this migration. 'CompetenceField.updated_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'DevelopmentPlanToUserRelation.created_by'
        raise RuntimeError("Cannot reverse this migration. 'DevelopmentPlanToUserRelation.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'EmployeeRole.created_by'
        raise RuntimeError("Cannot reverse this migration. 'EmployeeRole.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'File.created_by'
        raise RuntimeError("Cannot reverse this migration. 'File.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Employee.updated_by'
        raise RuntimeError("Cannot reverse this migration. 'Employee.updated_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Employee.created_by'
        raise RuntimeError("Cannot reverse this migration. 'Employee.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Role.created_by'
        raise RuntimeError("Cannot reverse this migration. 'Role.created_by' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Role.updated_by'
        raise RuntimeError("Cannot reverse this migration. 'Role.updated_by' and its values cannot be restored.")

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
        u'mus.action': {
            'Meta': {'object_name': 'Action'},
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Employee']"}),
            'follow_up_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'my_effort': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'my_needs': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '5', 'to': u"orm['mus.ActionStatus']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_updated_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mus.actioncomment': {
            'Meta': {'object_name': 'ActionComment'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comments'", 'null': 'True', 'to': u"orm['mus.Action']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_comment_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'follow_up_at': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.ActionStatus']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_comment_updated_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mus.actionstatus': {
            'Meta': {'object_name': 'ActionStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_da': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'mus.company': {
            'Meta': {'object_name': 'Company'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'company_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'company_updated_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mus.competence': {
            'Meta': {'object_name': 'Competence'},
            'competence_field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'competence_competence_field'", 'to': u"orm['mus.CompetenceField']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'competence_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'competence_updated_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mus.competencefield': {
            'Meta': {'object_name': 'CompetenceField'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['mus.Company']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'competence_field_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True'}),
            'development_plan_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.DevelopmentPlanType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_system': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "'da'", 'max_length': '15'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['mus.CompetenceField']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'competence_field_updated_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mus.developmentplan': {
            'Meta': {'object_name': 'DevelopmentPlan'},
            'competence_fields': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'development_plan_competence_fields'", 'symmetrical': 'False', 'to': u"orm['mus.CompetenceField']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'development_plan_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'employee_response_relation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'development_plan_employee'", 'to': u"orm['mus.DevelopmentPlanToUserRelation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "'da'", 'max_length': '15'}),
            'manager_response_relation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'development_plan_manager'", 'to': u"orm['mus.DevelopmentPlanToUserRelation']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Employee']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.DevelopmentPlanType']", 'null': 'True', 'blank': 'True'})
        },
        u'mus.developmentplantouserrelation': {
            'Meta': {'object_name': 'DevelopmentPlanToUserRelation'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'development_plan_user_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'finished_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'mus.developmentplantype': {
            'Meta': {'object_name': 'DevelopmentPlanType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'mus.employee': {
            'Meta': {'object_name': 'Employee'},
            'access_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Company']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'employee_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'development_plan_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.DevelopmentPlanType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "'da'", 'max_length': '15'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Employee']", 'null': 'True', 'blank': 'True'}),
            'newest_development_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.DevelopmentPlan']", 'null': 'True', 'blank': 'True'}),
            'plaintext_password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mus.Role']", 'through': u"orm['mus.EmployeeRole']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'employee_updated_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'employee_user'", 'to': u"orm['auth.User']"})
        },
        u'mus.employeerole': {
            'Meta': {'object_name': 'EmployeeRole'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'employee_role_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Role']"})
        },
        u'mus.file': {
            'Meta': {'object_name': 'File'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': u"orm['mus.Company']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'file_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['mus.FileBytes']", 'null': 'True', 'blank': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_size': ('django.db.models.fields.BigIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'files'", 'null': 'True', 'blank': 'True', 'to': u"orm['mus.Role']"})
        },
        u'mus.filebytes': {
            'Meta': {'object_name': 'FileBytes'},
            '_data': ('django.db.models.fields.TextField', [], {'db_column': "'data'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'mus.question': {
            'Meta': {'object_name': 'Question'},
            'allow_response': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'competence': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Competence']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'question_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('tinymce.models.HTMLField', [], {'max_length': '4000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'question_updated_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mus.questionresponse': {
            'Meta': {'object_name': 'QuestionResponse'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'question_response_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'development_plan_to_user_relation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question_response_development_plan_to_user_relation'", 'to': u"orm['mus.DevelopmentPlanToUserRelation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mus.Question']"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'question_response_updated_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mus.role': {
            'Meta': {'object_name': 'Role'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'role_created_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'role_updated_by'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['mus']