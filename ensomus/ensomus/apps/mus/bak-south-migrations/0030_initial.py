# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Role'
        db.create_table('mus_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='role_created_by',
                                                                                 to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='role_updated_by',
                                                                                 to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['Role'])

        # Adding model 'EmployeeRole'
        db.create_table('mus_employeerole', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.Employee'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.Role'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='employee_role_created_by',
                                                                   to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['EmployeeRole'])

        # Adding model 'Employee'
        db.create_table('mus_employee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='employee_user', to=orm['auth.User'])),
            ('manager',
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.Employee'], null=True, blank=True)),
            ('is_manager', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.Company'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='employee_created_by',
                                                                                 to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='employee_updated_by',
                                                                                 to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['Employee'])

        # Adding model 'Company'
        db.create_table('mus_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='company_created_by',
                                                                                 to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='company_updated_by',
                                                                                 to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['Company'])

        # Adding model 'CompetenceFieldCollectionCompetenceField'
        db.create_table('mus_competencefieldcollectioncompetencefield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competence_field_collection',
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.CompetenceFieldCollection'])),
            ('competence_field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.CompetenceField'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='competence_field_collection_competence_field_created_by', to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['CompetenceFieldCollectionCompetenceField'])

        # Adding model 'CompetenceQuestion'
        db.create_table('mus_competencequestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competence_field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.CompetenceField'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.Question'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='competence_question_created_by',
                                                                   to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['CompetenceQuestion'])

        # Adding model 'CompetenceField'
        db.create_table('mus_competencefield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=4000)),
            ('description', self.gf('tinymce.models.HTMLField')(null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='competence_field_created_by',
                                                                   to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='competence_field_updated_by',
                                                                   to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['CompetenceField'])

        # Adding model 'Competence'
        db.create_table('mus_competence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=4000)),
            ('description', self.gf('tinymce.models.HTMLField')(null=True)),
            ('competence_field',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='competence_competence_field',
                                                                   to=orm['mus.CompetenceField'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='competence_created_by',
                                                                                 to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='competence_updated_by',
                                                                                 to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['Competence'])

        # Adding model 'CompetenceFieldCollection'
        db.create_table('mus_competencefieldcollection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=4000)),
            ('description', self.gf('tinymce.models.HTMLField')(null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='competence_field_collection_created_by', to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='competence_field_collection_updated_by', to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['CompetenceFieldCollection'])

        # Adding model 'CompetenceFieldCollectionToCompanyRelation'
        db.create_table('mus_competencefieldcollectiontocompanyrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competence_field_collection',
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.CompetenceFieldCollection'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.Company'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='competence_field_collection_company_created_by', to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['CompetenceFieldCollectionToCompanyRelation'])

        # Adding model 'ActionKey'
        db.create_table('mus_actionkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')(null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_key_created_by',
                                                                                 to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_key_updated_by',
                                                                                 to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['ActionKey'])

        # Adding model 'Action'
        db.create_table('mus_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')(null=True)),
            ('action_key',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['mus.ActionKey'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_created_by',
                                                                                 to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_updated_by',
                                                                                 to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['Action'])

        # Adding model 'Question'
        db.create_table('mus_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('tinymce.models.HTMLField')(max_length=4000)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='question_created_by',
                                                                                 to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='question_updated_by',
                                                                                 to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['Question'])

        # Adding model 'CompetenceFieldCollectionToUserRelation'
        db.create_table('mus_competencefieldcollectiontouserrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competence_field_collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent',
                                                                                                  to=orm[
                                                                                                      'mus.CompetenceFieldCollection'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('finished_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('is_private', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='competence_field_collection_user_created_by', to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['CompetenceFieldCollectionToUserRelation'])

        # Adding model 'AssignmentKey'
        db.create_table('mus_assignmentkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('tinymce.models.HTMLField')(max_length=4000)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mus', ['AssignmentKey'])

        # Adding model 'Assignment'
        db.create_table('mus_assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')(null=True)),
            ('assignment_key', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignments',
                                                                                     to=orm['mus.AssignmentKey'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignment_created_by',
                                                                                 to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignment_updated_by',
                                                                                 to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['Assignment'])

        # Adding model 'AssignmentKeyToUserRelation'
        db.create_table('mus_assignmentkeytouserrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assignment_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.AssignmentKey'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('finished_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('is_private', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='assignment_key_to_user_relation_created_by', to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['AssignmentKeyToUserRelation'])

        # Adding model 'AssignmentResponse'
        db.create_table('mus_assignmentresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text_assignment', self.gf('django.db.models.fields.TextField')(null=True)),
            ('text_competence', self.gf('django.db.models.fields.TextField')(null=True)),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignment_responses',
                                                                                 to=orm['mus.Assignment'])),
            ('assignment_key_to_user_relation',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignment_responses',
                                                                   to=orm['mus.AssignmentKeyToUserRelation'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('mus', ['AssignmentResponse'])

        # Adding model 'DevelopmentPlan'
        db.create_table('mus_developmentplan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.Employee'])),
            ('manager_response_relation',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='development_plan_manager', to=orm[
                 'mus.CompetenceFieldCollectionToUserRelation'])),
            ('manager_assignment_key_relation', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='development_plan_manager_assignment_key_relation',
                to=orm['mus.AssignmentKeyToUserRelation'])),
            ('employee_response_relation',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='development_plan_employee', to=orm[
                 'mus.CompetenceFieldCollectionToUserRelation'])),
            ('employee_assignment_key_relation', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='development_plan_employee_assignment_key_relation',
                to=orm['mus.AssignmentKeyToUserRelation'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='development_plan_created_by',
                                                                   to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['DevelopmentPlan'])

        # Adding model 'ActionKeyToDevelopmentPlanRelation'
        db.create_table('mus_actionkeytodevelopmentplanrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.ActionKey'])),
            ('development_plan_relation', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='action_key_to_development_plan_relation', to=orm['mus.DevelopmentPlan'])),
            ('is_locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['ActionKeyToDevelopmentPlanRelation'])

        # Adding model 'ActionResponse'
        db.create_table('mus_actionresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_responses',
                                                                             to=orm['mus.Action'])),
            ('action_key_to_development_plan_relation',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_responses',
                                                                   to=orm['mus.ActionKeyToDevelopmentPlanRelation'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_response_created_by',
                                                                   to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_response_updated_by',
                                                                   to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['ActionResponse'])

        # Adding model 'QuestionResponse'
        db.create_table('mus_questionresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mus.Question'])),
            ('competence_field_collection_to_user_relation', self.gf('django.db.models.fields.related.ForeignKey')(
                related_name='question_response_competence_field_collection_to_user_relation',
                to=orm['mus.CompetenceFieldCollectionToUserRelation'])),
            ('text', self.gf('django.db.models.fields.TextField')(null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='question_response_created_by',
                                                                   to=orm['auth.User'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='question_response_updated_by',
                                                                   to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['QuestionResponse'])

        # Adding model 'FileBytes'
        db.create_table('mus_filebytes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_data', self.gf('django.db.models.fields.TextField')(db_column='data', blank=True)),
        ))
        db.send_create_signal('mus', ['FileBytes'])

        # Adding model 'File'
        db.create_table('mus_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('file_size', self.gf('django.db.models.fields.BigIntegerField')()),
            ('file_path', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('file',
             self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['mus.FileBytes'], null=True,
                                                                   blank=True)),
            ('company',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='files', to=orm['mus.Company'])),
            ('role',
             self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='files', null=True,
                                                                   blank=True, to=orm['mus.Role'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='file_created_by',
                                                                                 to=orm['auth.User'])),
        ))
        db.send_create_signal('mus', ['File'])


    def backwards(self, orm):
        # Deleting model 'Role'
        db.delete_table('mus_role')

        # Deleting model 'EmployeeRole'
        db.delete_table('mus_employeerole')

        # Deleting model 'Employee'
        db.delete_table('mus_employee')

        # Deleting model 'Company'
        db.delete_table('mus_company')

        # Deleting model 'CompetenceFieldCollectionCompetenceField'
        db.delete_table('mus_competencefieldcollectioncompetencefield')

        # Deleting model 'CompetenceQuestion'
        db.delete_table('mus_competencequestion')

        # Deleting model 'CompetenceField'
        db.delete_table('mus_competencefield')

        # Deleting model 'Competence'
        db.delete_table('mus_competence')

        # Deleting model 'CompetenceFieldCollection'
        db.delete_table('mus_competencefieldcollection')

        # Deleting model 'CompetenceFieldCollectionToCompanyRelation'
        db.delete_table('mus_competencefieldcollectiontocompanyrelation')

        # Deleting model 'ActionKey'
        db.delete_table('mus_actionkey')

        # Deleting model 'Action'
        db.delete_table('mus_action')

        # Deleting model 'Question'
        db.delete_table('mus_question')

        # Deleting model 'CompetenceFieldCollectionToUserRelation'
        db.delete_table('mus_competencefieldcollectiontouserrelation')

        # Deleting model 'AssignmentKey'
        db.delete_table('mus_assignmentkey')

        # Deleting model 'Assignment'
        db.delete_table('mus_assignment')

        # Deleting model 'AssignmentKeyToUserRelation'
        db.delete_table('mus_assignmentkeytouserrelation')

        # Deleting model 'AssignmentResponse'
        db.delete_table('mus_assignmentresponse')

        # Deleting model 'DevelopmentPlan'
        db.delete_table('mus_developmentplan')

        # Deleting model 'ActionKeyToDevelopmentPlanRelation'
        db.delete_table('mus_actionkeytodevelopmentplanrelation')

        # Deleting model 'ActionResponse'
        db.delete_table('mus_actionresponse')

        # Deleting model 'QuestionResponse'
        db.delete_table('mus_questionresponse')

        # Deleting model 'FileBytes'
        db.delete_table('mus_filebytes')

        # Deleting model 'File'
        db.delete_table('mus_file')


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
            'title': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'assignment_updated_by'", 'to': "orm['auth.User']"})
        },
        'mus.assignmentkey': {
            'Meta': {'object_name': 'AssignmentKey'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('tinymce.models.HTMLField', [], {'max_length': '4000'})
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