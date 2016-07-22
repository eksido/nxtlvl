from django.core.urlresolvers import reverse
from models import Company, Employee, EmployeeRole, Role
from models import CompetenceField, Competence
from models import DevelopmentPlanToUserRelation, QuestionResponse, Question, DevelopmentPlan, DevelopmentPlanType, \
    ReminderTemplate
from models import Action, ActionComment, ActionStatus, File, FileBytes
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
from django.utils.html import format_html


class TinyMCEFlatPageAdmin(FlatPageAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 60, 'rows': 20},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ))
        return super(TinyMCEFlatPageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

        # class Media:

        # js = (
        #        '/static/js/tiny_mce/tiny_mce.js',
        #        )


class CreatedByUpdatedByModelBase(admin.ModelAdmin):
    exclude = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


class CreatedByModelBase(admin.ModelAdmin):
    exclude = ('created_by',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()


class ActionAdmin(CreatedByUpdatedByModelBase):
    pass


class ActionCommentAdmin(CreatedByUpdatedByModelBase):
    pass


class ActionStatusAdmin(CreatedByUpdatedByModelBase):
    pass


class CompanyAdmin(CreatedByUpdatedByModelBase):
    pass


class EmployeeAdmin(CreatedByUpdatedByModelBase):
    pass


class RoleAdmin(CreatedByUpdatedByModelBase):
    pass


class EmployeeRoleAdmin(CreatedByModelBase):
    pass


class QuestionAdmin(CreatedByUpdatedByModelBase):
    list_filter = ('competence',)
    list_display = ('formatted_title', 'competence')

    def formatted_title(self, obj):
        return format_html(obj.title)

    formatted_title.short_description = 'Title'


class CompetenceFieldAdmin(CreatedByUpdatedByModelBase):
    list_display = (
        'title', 'development_plan_type', 'language_code', 'is_manager', 'company', 'competence_count', 'competences')

    def competences(self, instance):
        return '<a href="/admin/mus/competence/?competence_field__id__exact=%d">%s</a>' % (instance.id, "Competences")

    competences.allow_tags = True


class CompetenceAdmin(CreatedByUpdatedByModelBase):
    list_display = ('__unicode__', 'question_count', 'questions')
    list_filter = ('competence_field',)

    def questions(self, instance):
        return '<a href="/admin/mus/question/?competence__id__exact=%d">%s</a>' % (instance.id, "Questions")

    questions.allow_tags = True


class DevelopmentPlanToUserRelationAdmin(CreatedByModelBase):
    pass


class DevelopmentPlanAdmin(CreatedByModelBase):
    pass


class DevelopmentPlanTypeAdmin(CreatedByModelBase):
    pass


class QuestionResponseAdmin(CreatedByUpdatedByModelBase):
    pass


class FileAdmin(admin.ModelAdmin):
    exclude = ('file_name', 'mime_type', 'file_size', 'file', 'created_by')
    actions = ['delete_model']

    def get_actions(self, request):
        actions = super(FileAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        upload_file = request.FILES['file_path']
        file_bytes = FileBytes()
        file_bytes.set_data(upload_file.read())
        file_bytes.save()
        obj.file_name = upload_file.name
        obj.mime_type = upload_file.content_type
        obj.file_size = upload_file.size
        obj.file = file_bytes
        admin.ModelAdmin.save_model(self, request, obj, form, change)

    def delete_model(self, request, queryset):
        for obj in queryset:
            try:
                file_bytes = FileBytes.objects.get(pk=obj.file.pk)
                file_bytes.delete()
                admin.ModelAdmin.delete_model(self, request, obj)
            except FileBytes.DoesNotExist:
                pass

    delete_model.short_description = u'Slet valgte filer'


class ReminderTempateAdmin(admin.ModelAdmin):
    pass


admin.site.register(File, FileAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(ActionComment, ActionCommentAdmin)
admin.site.register(CompetenceField, CompetenceFieldAdmin)
admin.site.register(Competence, CompetenceAdmin)
admin.site.register(DevelopmentPlanToUserRelation, DevelopmentPlanToUserRelationAdmin)
admin.site.register(DevelopmentPlan, DevelopmentPlanAdmin)
admin.site.register(DevelopmentPlanType, DevelopmentPlanTypeAdmin)
admin.site.register(QuestionResponse, QuestionResponseAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(EmployeeRole, EmployeeRoleAdmin)
admin.site.register(ActionStatus, ActionStatusAdmin)
admin.site.register(ReminderTemplate, ReminderTempateAdmin)