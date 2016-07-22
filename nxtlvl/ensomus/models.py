"""
This module contains the models for NXT LVL
"""
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
# from django_mailer_plus import send_mail
from mailer import send_mail
import datetime
from django.conf import settings
from django.template import loader, Context
import base64
from django.db.models import Q
from django.db import transaction
from django.utils.encoding import smart_str
from util import safeHtmlString, replaceAllText, my_decrypt, write_pdf, generate_password, my_encrypt
from django.utils.translation import ugettext_lazy as _, get_language, activate
from django.utils import translation
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.html import strip_tags
from django.utils.timezone import now
import re
import hashlib
from threadlocals.threadlocals import get_current_request


class Role(models.Model):
    """
    Roles for employee
    """
    name = models.CharField(verbose_name=_(u"name"), max_length=255)
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='role_created_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    updated_by = models.ForeignKey(User, verbose_name=_(u"updated by"), related_name='role_updated_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'role')
        verbose_name_plural = _(u'roles')

    def __unicode__(self):
        return self.name[:50]


class EmployeeRole(models.Model):
    """
    Employee/Role relation
    """
    employee = models.ForeignKey('Employee', verbose_name=_(u"employee"))
    role = models.ForeignKey('Role', verbose_name=_(u"role"))
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='employee_role_created_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'employee role')
        verbose_name_plural = _(u'employee roles')

    def __unicode__(self):
        return u'%s - (%s)' % (self.employee.user.get_full_name(), self.role.name)


class DevelopmentPlanType(models.Model):
    """
    Types of development plan
    """
    name = models.CharField(max_length=255)
    company = models.ForeignKey('Company', verbose_name=_(u'company'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'development plan type')
        verbose_name_plural = _(u'development plan types')

    def __unicode__(self):
        return u'%s' % safeHtmlString(self.name, 255)


class Employee(models.Model):
    """
    Employee in a company
    """
    user = models.ForeignKey(User, related_name='employee_user', verbose_name=_("user"))
    development_plan_type = models.ForeignKey(DevelopmentPlanType, verbose_name=_("development plan type"), null=True,
                                              blank=True)
    newest_development_plan = models.ForeignKey('DevelopmentPlan', verbose_name=_(u'newest_development_plan'),
                                                null=True, blank=True)
    manager = models.ForeignKey('self', verbose_name=_(u"manager"), null=True, blank=True)
    is_manager = models.BooleanField(verbose_name=_(u"is manager"), default=False)
    company = models.ForeignKey('Company', verbose_name=_(u"company"))
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='employee_created_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    updated_by = models.ForeignKey(User, verbose_name=_(u"updated by"), related_name='employee_updated_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)
    language_code = models.CharField(max_length=15, verbose_name=_(u'language'), choices=settings.LANGUAGES,
                                     default=settings.LANGUAGE_CODE)
    plaintext_password = models.CharField(max_length=200, blank=True)
    access_code = models.CharField(max_length=200, blank=True)
    roles = models.ManyToManyField(
        Role,
        through=EmployeeRole)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _(u'employee')
        verbose_name_plural = _(u'employees')

    def __unicode__(self):
        if self.is_manager:
            return u'%s (%s)' % (self.user.get_full_name(), _(u'Manager'))
        return u'%s' % self.user.get_full_name()


    def hasAccessTo(self, target):
        """

        Check if this employee has access to the target.

        Parameters
        target : Employee
            The target of the access check. Can be a pk as well.
        """

        if self.isEnsoUser():
            return True

        if isinstance(target, Employee):
            targetEmployee = target
        else:
            targetEmployee = Employee.objects.get(pk=int(target))
            assert isinstance(targetEmployee, Employee)

        if not self.pk == int(targetEmployee.pk):
            if not self.is_manager or not self.company.pk == targetEmployee.company.pk:
                if not self.isCompanySuperUserOrHigher():
                    return False

        return True


    @staticmethod
    def isValidUsername(username):
        """
        Checks the username against nxtlvl rules

        :param username: str
        :return: bool
        """
        r = re.compile('^[a-z0-9_\-\.]+$', re.I)

        return True if r.match(username) else False

    def getAccessCode(self):
        if self.access_code == "":
            access_code = hashlib.md5("%s%s" % (self.user.username, settings.SECRET_KEY)).hexdigest()
            self.access_code = access_code
            self.save()
        return self.access_code

    def getMyEmployees(self, manager=None):
        """
        Get list of employees with given manager or self as manager
        """
        if manager is None:
            manager = self
        employees = list()
        for employee in self.getMyEmployeesQueryset(manager):
            employees.append(employee)
        return employees

    def getMyEmployeesQueryset(self, manager=None):
        """
        Get queryset of employe with given manager or self as manager
        """
        if manager is None:
            manager = self
        return Employee.objects.filter(manager__pk=manager.pk, company__pk=self.company.pk).order_by('-is_manager',
                                                                                                     'user__last_name',
                                                                                                     'user__first_name')

    def getEmployees(self):
        """
        Get list of employees in the same company
        """
        employees = list()
        for manager in Employee.objects.filter(company__pk=self.company.pk, manager_id=None):
            employees += self.getMyEmployees(manager=manager)
        return employees

    @transaction.atomic
    def createDevelopmentPlan(self, competence_fields, current_user, email_text, template):
        """
        Create a development plan containing given competence fields, create it by current user and send an email to self with email_text
        """
        if not self.canAssociateNewPlan():
            return None
        development_plan = DevelopmentPlan()
        development_plan.owner = self
        development_plan.type = self.development_plan_type
        development_plan.language_code = self.language_code
        if self.manager:
            manager_user = self.manager.user
        else:
            manager_user = current_user
        development_plan.employee_response_relation = DevelopmentPlanToUserRelation.objects.create(
            user=self.user,
            created_by=current_user
        )
        development_plan.manager_response_relation = DevelopmentPlanToUserRelation.objects.create(
            user=manager_user,
            created_by=current_user
        )
        development_plan.created_by = current_user

        development_plan.employee_response_relation.save()
        development_plan.manager_response_relation.save()
        development_plan.save()
        self.newest_development_plan = development_plan
        self.save()

        development_plan.competence_fields = competence_fields

        development_plan.save()
        self._sendNotification(self.user, current_user, email_text, template)
        return development_plan

    def _sendNotification(self, user, current_user, email_text, template_code):
        """
        Send a notification to user from current user based on template
        """
        template = loader.get_template('mus/emails/attach_development_plan_%s.html' % template_code)
        if template_code == "da":
            subject = "NXT LVL - Udfyld forberedelsesguide"
        elif template_code == "en":
            subject = "NXT LVL - Fill out preparation guide"
        else:
            raise Exception("Unknown template: %s" % template_code)
        employee = user.employee_user.first()
        if employee.plaintext_password == '':
            password = generate_password(8)
            employee.plaintext_password = my_encrypt(password)
            user.set_password(password)
            user.save()
            employee.save()
        else:
            password = my_decrypt(user.employee_user.first().plaintext_password)
        htmlbody = template.render(
            Context({
                'user': user,
                'text': email_text,
                'sender': current_user,
                'password': password
            })
        )
        send_mail(
            subject,
            strip_tags(htmlbody),
            settings.DEFAULT_FROM_MAIL,
            ("%s <%s>" % (user.get_full_name(), user.email),),
            html_message=htmlbody
        )

    def getDevelopmentPlans(self):
        """
        Get all development plans for self, newest first
        """
        query_set = None
        query_set = DevelopmentPlan.objects.filter(owner__pk=self.pk).exclude(deleted=True)
        return query_set.order_by('-created_at')

    def to_json(self):
        """
        Convert self to json serializable dict

        is it used?
        """
        return dict(
            id=self.pk,
            user=dict(id=self.user.id, name=self.user.get_full_name()),
            manager=(
                dict() if self.manager == None else dict(id=self.manager.id, name=self.manager.user.get_full_name())),
            is_manager=self.is_manager,
            company=self.company.to_json()
        )

    def to_dict(self):
        """
        Convert self to json serializable dict
        """
        employee = dict(
            id=self.pk,
            user_id=self.user.pk,
            name=self.user.get_full_name(),
            email=self.user.email,
            development_plan_type=self.development_plan_type.name,
            is_manager=self.is_manager,
            employees=[employee.to_dict() for employee in self.getMyEmployees()],
            actionstatus=self.getActionStatus(),
        )
        dps = self.getDevelopmentPlans()
        if dps.exists():
            employee['development_plan'] = dps[0].to_dict()

        return employee

    def hasManager(self):
        """
        Does self have a manager?
        """
        return self.manager != None

    def isCompanySuperUserOrHigher(self):
        """
        Is self company super user or higher privileges
        """
        return self.roles.count() > 0

    def isEnsoUser(self):
        """
        Is self enso user
        """
        return self.roles.count() > 0 and self.roles.filter(name=u'Enso-bruger').exists()

    def getSchemes(self, my_own=None):
        """
        ?

        is it used?
        """
        if my_own is None or my_own:
            competence_field_collection_to_user_relations = CompetenceFieldCollectionToUserRelation.objects.filter(
                user__pk=self.user.pk
            ).order_by('finished_at').order_by('created_at')
        else:
            user_ids = Employee.objects.filter(manager__user__pk=self.user.pk).values_list('user__pk')
            competence_field_collection_to_user_relations = CompetenceFieldCollectionToUserRelation.objects.filter(
                user__pk__in=user_ids
            ).exclude(finished_at=None).order_by('finished_at').order_by('created_at')
        competence_field_collections = list()
        for competence_field_collection_to_user_relation in competence_field_collection_to_user_relations:
            collection = {
                'pk': competence_field_collection_to_user_relation.pk,
                'finished_at': competence_field_collection_to_user_relation.finished_at,
                'created_at': competence_field_collection_to_user_relation.created_at,
                'employee_name': competence_field_collection_to_user_relation.user.get_full_name(),
                'competence_field_collection': competence_field_collection_to_user_relation.competence_field_collection,
                'action_key': None  # ActionKeyToCompetenceFieldCollectionToUserRelation.objects.get(
                # competence_field_collection_to_user_relation=competence_field_collection_to_user_relation
                # ).action_key
            }
            competence_field_collections.append(collection)
        return competence_field_collections

    def getQuestionnaire(self, competence_field_collection_to_user_relation_id, respect_finished_at=True):
        """
        ?

        is it used?
        """
        competence_field_collection_to_user_relation = CompetenceFieldCollectionToUserRelation.objects.get(
            pk=competence_field_collection_to_user_relation_id
        )
        question_response = None
        if not respect_finished_at:
            question_response = competence_field_collection_to_user_relation.getQuestionResponses(respect_finished_at)
        elif not competence_field_collection_to_user_relation.finished_at is None:
            question_response = competence_field_collection_to_user_relation.getQuestionResponses()
        return {
            'pk': competence_field_collection_to_user_relation.pk,
            'competence_field_collection': competence_field_collection_to_user_relation.competence_field_collection,
            'competence_field_collection_to_user_relation': competence_field_collection_to_user_relation,
            'question_response': question_response
        }

    def canAssociateNewPlan(self):
        """
        Is it possible to associate a new development plan to self?
        """
        return DevelopmentPlan.objects.filter(owner__pk=self.pk, employee_response_relation__finished_at=None,
                                              manager_response_relation__finished_at=None).exclude(
            deleted=True).count() == 0


    def getActionStatus(self):
        """
        Get status of action key
        """
        status = dict(number=2, description=_("Complete: Currently no issues"))
        actions = self.action_set.all()
        if not actions.exists():
            return dict(number=0, description=_("No actions exists"))
        for action in actions:
            if action.status and action.status.pk == 5:
                return dict(number=0, description=_("Actions not approved"))
        return status

    def isManager(self):
        """
        Is this user a manager
        """
        return self.is_manager == 1


class Company(models.Model):
    """
    A company (client of NXT LVL)
    """
    name = models.CharField(verbose_name=_(u"name"), max_length=255)
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='company_created_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    updated_by = models.ForeignKey(User, verbose_name=_(u"updated by"), related_name='company_updated_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'company')
        verbose_name_plural = _(u'companies')

    def __unicode__(self):
        return safeHtmlString(self.name, 50)

    """
    Convert to json serializable dict
    """

    def to_json(self):
        return dict(
            id=self.pk,
            name=self.name
        )

    def getTopManagers(self):
        """
        Get top managers in the company of self
        """
        return Employee.objects.filter(company__pk=self.pk, manager_id=None)

    def toString(self):
        return self.__unicode__()


class CompetenceField(models.Model):
    """
    A competence field is a part of the competence key in a development plan
    """
    title = models.CharField(verbose_name=_(u"title"), max_length=4000)
    description = HTMLField(verbose_name=_(u"description"), null=True)
    company = models.ForeignKey(Company, verbose_name=_(u"company"), null=True, blank=True, default=None)
    is_system = models.BooleanField(verbose_name=_(u"is system"), default=False)
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='competence_field_created_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    updated_by = models.ForeignKey(User, verbose_name=_(u"updated by"), related_name='competence_field_updated_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', verbose_name=_(u'parent'), related_name='children', null=True, blank=True,
                               limit_choices_to={'parent': None})
    development_plan_type = models.ForeignKey(DevelopmentPlanType, verbose_name=_(u'development plan type'))
    language_code = models.CharField(max_length=15, verbose_name=_(u'language'), choices=settings.LANGUAGES,
                                     default=settings.LANGUAGE_CODE)
    is_manager = models.BooleanField(default=False, verbose_name=_(u'for manager'))
    sort_order = models.IntegerField(verbose_name=_(u"sort order"), )

    class Meta:
        verbose_name = _(u'competence field')
        verbose_name_plural = _(u'competence fields')

    def __unicode__(self):
        return u'%s - %s - %s%s - %s' % (
            safeHtmlString(self.title, 20), safeHtmlString(self.development_plan_type.name, 50), self.language_code,
            self.company and " - %s" % self.company or "", self.is_manager and _("manager") or "")

    def getCompetences(self):
        """
        Get related competences
        """
        return self.competence_competence_field.all().order_by('sort_order')

    def getDescription(self):
        description = re.sub("\[box\]", "<div class=\"box\">", self.description)
        description = re.sub("\[/box\]", "</div>", description)
        return description

    def cloneTo(self, cddtype):
        ncf = CompetenceField()
        ncf.title = self.title
        ncf.description = self.description
        ncf.is_system = self.is_system
        ncf.created_at = self.created_at
        ncf.created_by = self.created_by
        ncf.updated_at = self.updated_at
        ncf.updated_by = self.updated_by
        if self.parent:
            ncf.parent = self.parent
        else:
            ncf.parent = self
        ncf.development_plan_type = cddtype
        ncf.language_code = self.language_code
        ncf.is_manager = self.is_manager
        ncf.sort_order = self.sort_order
        ncf.save()
        for competence in self.getCompetences():
            competence.cloneTo(ncf)

    def to_dict(self):
        """
        Convert to dictionary
        """
        return dict(
            title=self.title,
            description=self.description.replace("[box]", '<div class="well">').replace("[/box]", '</div>')
        )


    def competence_count(self):
        return self.competence_competence_field.count()

    def toString(self):
        return self.__unicode__()

    def toString_is_manager(self):
        text = 'Not manager'
        if self.is_manager:
            text = 'Manager'
            return text
        return text


class Competence(models.Model):
    """
    A competence is a subpart of a competence field
    """
    title = models.CharField(verbose_name=_(u"title"), max_length=4000)
    description = HTMLField(verbose_name=_(u"description"), null=True)
    competence_field = models.ForeignKey(CompetenceField, verbose_name=_(u"competence field"),
                                         related_name='competence_competence_field')
    sort_order = models.IntegerField(verbose_name=_(u"sort order"), )
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='competence_created_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    updated_by = models.ForeignKey(User, verbose_name=_(u"updated by"), related_name='competence_updated_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'competence')
        verbose_name_plural = _(u'competences')

    def cloneTo(self, competence_field):
        nc = Competence()
        nc.title = self.title
        nc.description = self.description
        nc.competence_field = competence_field
        nc.sort_order = self.sort_order
        nc.created_at = self.created_at
        nc.created_by = self.created_by
        nc.updated_at = self.updated_at
        nc.updated_by = self.updated_by
        nc.save()
        for question in self.getQuestions():
            question.cloneTo(nc)

    def to_dict(self, development_plan_user=None):
        """
        Convert to dictionary
        """
        competence = {
            'description': self.description.replace("[box]", '<div class="well">').replace("[/box]", '</div>'),
            'title': self.title,
            'questions': [],
        }
        for question in self.question_set.all().order_by('sort_order'):
            competence['questions'].append(question.to_dict(development_plan_user))
        return competence

    def getQuestions(self):
        """
        Get related questions
        """
        return self.question_set.all().order_by('sort_order')

    def getStatus(self, development_plan_user):
        """
        Get status of competence, 0 is not finished, 1 is partial finished and 2 is finished
        """
        amount = 0
        total = self.question_set.count()
        for question in self.question_set.all():
            if question.allow_response and development_plan_user.getResponse(question.pk):
                amount = amount + 1
        if total == amount:
            return 2
        elif amount == 0:
            return 0
        else:
            return 0

    def question_count(self):
        return self.question_set.count()

    def getDescription(self):
        description = re.sub("\[box\]", "<div class=\"box\">", self.description)
        description = re.sub("\[/box\]", "</div>", description)
        return description

    def __unicode__(self):
        return u'%s (%s)' % (
            safeHtmlString(self.title, 50),
            safeHtmlString(self.competence_field.toString(), 50))


class ActionStatus(models.Model):
    """
    Possible statuses for an action
    """
    name_da = models.CharField(verbose_name=_(u'name_da'), max_length=30)
    name_en = models.CharField(verbose_name=_(u'name_en'), max_length=30)

    class Meta:
        verbose_name = _(u'action status')
        verbose_name_plural = _(u'action statuses')

    def __unicode__(self):
        if get_language() == 'da':
            return u'%s' % safeHtmlString(self.name_da, 100)
        else:
            return u'%s' % safeHtmlString(self.name_en, 100)

    def __str__(self):
        return self.__unicode__()


class Action(models.Model):
    """
    Each employee has a number of action representing their goals
    """
    title = models.TextField(verbose_name=_(u"title"))
    description = models.TextField(verbose_name=_(u"description"), null=True, blank=True)
    my_effort = models.TextField(verbose_name=_(u"my contribution"), null=True, blank=True)
    my_needs = models.TextField(verbose_name=_(u"my need for support"), null=True, blank=True)
    approved_at = models.DateTimeField(verbose_name=_(u"approved at"), null=True, blank=True)
    follow_up_at = models.DateField(verbose_name=_(u"follow up at"), null=True, blank=True)
    status = models.ForeignKey(ActionStatus, verbose_name=_(u"status"), null=True, blank=True, default=5)
    employee = models.ForeignKey(Employee, verbose_name=_(u"employee"))
    sort_order = models.IntegerField(verbose_name=_(u"sort order"))
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='action_created_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    updated_by = models.ForeignKey(User, verbose_name=_(u"updated by"), related_name='action_updated_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=1, null=True)
    difficulty = models.IntegerField(null=True)

    TYPE_A = 'A'
    TYPE_B = 'B'
    TYPE_C = 'C'

    DIFFICULTY_LOW = 1
    DIFFICULTY_MEDIUM = 2
    DIFFICULTY_HIGH = 3

    class Meta:
        verbose_name = _(u'action')
        verbose_name_plural = _(u'actions')

    def getComments(self):
        """
        Get related comments, newest first
        """
        return self.comments.order_by('-id')

    def getLatestComment(self):
        """
        Get latest comment
        """
        comments = self.comments.order_by('-id')
        if comments.exists():
            return comments[0]
        return None

    def __unicode__(self):
        return u'%s' % safeHtmlString(self.title, 100)

    def send_approval_notification(self):
        if self.created_by == self.employee.user:

            language_code = self.employee.manager.language_code
            template = loader.get_template('mus/emails/approve_employee_action_%s.html' % language_code)
            if language_code == 'da':
                subject = "Din medarbejder har oprettet en indsats og venter godkendelse"
            elif language_code == 'en':
                subject = "Your employee has created a contribution and awaits approval"
            else:
                raise PermissionDenied()
            htmlbody = template.render(
                Context({
                    'employee_user': self.employee.user,
                    'user': self.employee.manager.user
                })
            )
            send_mail(
                subject,
                strip_tags(htmlbody),
                settings.DEFAULT_FROM_MAIL,
                ("%s <%s>" % (self.employee.manager.user.get_full_name(), self.employee.manager.user.email),),
                html_message=htmlbody
            )
        else:
            language_code = self.employee.language_code
            template = loader.get_template('mus/emails/approve_manager_action_%s.html' % language_code)
            if language_code == 'da':
                subject = "Din leder har oprettet en indsats og venter godkendelse"
            elif language_code == 'en':
                subject = "Your manager has created a contribution and awaits approval"
            else:
                raise PermissionDenied()
            if self.employee.manager:
                manager_user = self.employee.manager.user
            else:
                manager_user = self.created_by
            htmlbody = template.render(
                Context({
                    'manager_user': manager_user,
                    'user': self.employee.user,
                })
            )
            send_mail(
                subject,
                strip_tags(htmlbody),
                settings.DEFAULT_FROM_MAIL,
                ("%s <%s>" % (self.employee.user.get_full_name(), self.employee.user.email),),
                html_message=htmlbody
            )

    def __str__(self):
        return self.__unicode__()


    def getDifficultyText(self):
        return {
            Action.DIFFICULTY_LOW: _(u'Low'),
            Action.DIFFICULTY_MEDIUM: _(u'Medium'),
            Action.DIFFICULTY_HIGH: _(u'High'),
            None: ''
        }[self.difficulty]

    def getTypeText(self):
        return {
            Action.TYPE_A: _('Action type A'),
            Action.TYPE_B: _('Action type B'),
            Action.TYPE_C: _('Action type C'),
            None: ''
        }[self.type]

    @staticmethod
    def getDifficultyChoices():
        return (
            (Action.DIFFICULTY_LOW, _(u'Low')),
            (Action.DIFFICULTY_MEDIUM, _(u'Medium')),
            (Action.DIFFICULTY_HIGH, _(u'High')),
        )


    @staticmethod
    def getTypeChoices():
        return (
            (Action.TYPE_A, _('Action type A')),
            (Action.TYPE_B, _('Action type B')),
            (Action.TYPE_C, _('Action type C')),
        )


class ActionComment(models.Model):
    """
    Actions can have comments
    """
    action = models.ForeignKey(Action, verbose_name=_(u'action'), null=True, blank=True, related_name='comments')
    text = models.TextField(verbose_name=_(u"text"))
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='action_comment_created_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    updated_by = models.ForeignKey(User, verbose_name=_(u"updated by"), related_name='action_comment_updated_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)
    follow_up_at = models.DateField(verbose_name=_(u"follow up at"), null=True, blank=True, default=None)
    status = models.ForeignKey(ActionStatus, verbose_name=_(u"status"), null=True, blank=True)

    class Meta:
        verbose_name = _(u'action comment')
        verbose_name_plural = _(u'action comments')

    def sendCommentNotification(self, type, recipient, peer):
        """
        Sends an email to the recipient, that a comment has been added by peer.

        :type type: str
        1 for mail to employee, 2 = manager

        :type recipient: User
        :type peer: User

        """

        rcpt_emp = Employee.objects.get(user=recipient)
        """:type Employee"""

        language_code = rcpt_emp.language_code

        if type == 1:
            tmpl_file = 'mus/emails/action_comment_employee_%s.html' % language_code

            if language_code == 'da':
                subject = "Din medarbejder har en kommentar og venter godkendelse"
            else:
                subject = "Your employee has added a comment and awaits approval"

        else:
            tmpl_file = 'mus/emails/action_comment_manager_%s.html' % language_code

            if language_code == 'da':
                subject = "Din leder har en kommentar og venter godkendelse"
            else:
                subject = "Your manager has added a comment and awaits approval"

        template = loader.get_template(tmpl_file)

        htmlbody = template.render(
            Context({
                'peer': peer,
                'recipient': recipient,
                'comment': self.text
            })
        )

        send_mail(
            subject,
            strip_tags(htmlbody),
            settings.DEFAULT_FROM_MAIL,
            ("%s <%s>" % (recipient.get_full_name(), recipient.email),),
            html_message=htmlbody
        )


    def __unicode__(self):
        return u'%s' % safeHtmlString(self.text, 100)

    def __str__(self):
        return self.__unicode__()


class Question(models.Model):
    """
    A competence has questions
    """
    title = HTMLField(verbose_name=_(u"title"), max_length=4000)
    competence = models.ForeignKey('Competence', verbose_name=_(u"competence"))
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='question_created_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    updated_by = models.ForeignKey(User, verbose_name=_(u"updated by"), related_name='question_updated_by', blank=True,
                                   null=True, on_delete=models.SET_NULL)
    sort_order = models.IntegerField(verbose_name=_(u"sort order"))
    allow_response = models.BooleanField(verbose_name=_(u'allow response'), default=True)

    class Meta:
        verbose_name = _(u'question')
        verbose_name_plural = _(u'questions')

    def cloneTo(self, competence):
        nq = Question()
        nq.title = self.title
        nq.competence = competence
        nq.created_at = self.created_at
        nq.created_by = self.created_by
        nq.updated_at = self.updated_at
        nq.updated_by = self.updated_by
        nq.sort_order = self.sort_order
        nq.allow_response = self.allow_response
        nq.save()

    def to_dict(self, development_plan_user=None):
        """
        Convert to dictionary
        """
        result = dict(
            pk=self.pk,
            title=self.title.replace("[box]", '<div class="well">').replace("[/box]", '</div>'),
            allow_response=self.allow_response
        )
        if development_plan_user:
            result['response'] = development_plan_user.getResponse(self.pk)
        return result

    def __unicode__(self):
        return u'%s' % safeHtmlString(self.title, 50)


class DevelopmentPlanToUserRelation(models.Model):
    """
    Relation between user(employee/manager) and development plan
    """
    user = models.ForeignKey(User, verbose_name=_(u"user"))
    finished_at = models.DateTimeField(verbose_name=_(u"finished at"), null=True, default=None, blank=True)
    is_private = models.BooleanField(verbose_name=_(u"is private"), default=True)
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='development_plan_user_created_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'development plan to user relation')
        verbose_name_plural = _(u'development plan to user relations')

    def __unicode__(self):
        return u'%s for %s' % (self.getDevelopmentPlan(), self.user.get_full_name())

    def to_dict(self):
        """
        Convert to dictionary
        """
        return dict(
            id=self.pk,
            user_id=self.user.pk,
            finished_at=self.finished_at != None,
            not_finished_text=_("Hidden"),
            is_private=self.is_private,
            status=self.getStatus()
        )

    def isManagers(self):
        """
        Is the manager's development plan?
        """
        plans = self.development_plan_manager.all()
        return len(plans) != 0

    def getDevelopmentPlan(self):
        """
        Get related development plan
        """
        plans = self.development_plan_manager.all()
        if len(plans) == 0:
            plans = self.development_plan_employee.all()
            if len(plans) == 0:
                return None
        return plans[0];

    def getPDFfile(self):
        development_plan = self.getDevelopmentPlan()
        filename = "%s/%s" % (settings.FILES_ROOT, "plans/%d.pdf" % self.pk)
        try:
            with open(filename):
                return filename
        except IOError:
            pass
        activate(development_plan.language_code.lower())
        write_pdf(
            'mus/development_plan_pdf.html',
            {
                'company': development_plan.owner.company,
                'owner_name': development_plan.owner,
                'extension': "%s_%s%s" % (
                development_plan.language_code.lower(), development_plan.type.name.lower()[:-3],
                self.isManagers() and "_manager" or ""),
                'development_plan_user': self,
                'assignment_competence': development_plan.getAssignmentCompetence(self),
                'evaluation_competence': development_plan.getEvaluationCompetence(self),
                'competence_fields': development_plan.getCompetenceFields(self),
            },
            filename
        )
        return filename

    def getReadStatus(self, link):
        try:
            DevelopmentPlanPageStatus.objects.get(pagelink=link, development_plan_relation=self)
            return 2
        except DevelopmentPlanPageStatus.DoesNotExist:
            return 0

    def getStates(self):
        """
        Get the states for the progress bar as dictionary
        """
        dp = self.getDevelopmentPlan()
        translation.activate(dp.language_code)
        result = list()
        result.append({'name': 'Intro', 'status': [{'link': '/', 'value': 2}]})
        status = list()
        competence = dp.getAssignmentCompetence(self)
        if competence:
            status.append(
                {'link': '/' + competence.title, 'value': competence.getStatus(self), 'competence_id': competence.pk})
            result.append({'name': competence.title, 'status': status})

        result.append({'name': _(u'competence key').capitalize(),
                       'status': [{'link': '/intro-competence', 'value': self.getReadStatus('/intro-competence')}]})
        for competence_field in dp.getCompetenceFields(self):
            status = list()
            status.append({'link': '/intro-' + competence_field.title,
                           'value': self.getReadStatus('/intro-' + competence_field.title),
                           'competence_field_id': competence_field.pk})
            for competence in competence_field.getCompetences():
                status.append({'link': '/' + competence.title, 'value': competence.getStatus(self),
                               'competence_id': competence.pk})
            result.append({'name': competence_field.title, 'status': status})
        status = list()
        competence = dp.getEvaluationCompetence(self)
        status.append(
            {'link': '/' + competence.title, 'value': competence.getStatus(self), 'competence_id': competence.pk})
        result.append({'name': competence.title, 'status': status})
        result.append({'name': _('end').capitalize(), 'status': [
            {'link': '/summary', 'value': self.getReadStatus('/summary')},
            {'link': '/end', 'value': self.getReadStatus('/end')}
        ]})
        return result

    def getCompetencesAsDict(self):
        """
        Get comptetences with questiosn and answers as dict
        """
        competence_list = list()
        dp = self.getDevelopmentPlan()
        competence = dp.getAssignmentCompetence(self)
        competence_list.append(competence.to_dict(self))
        for competence_field in dp.getCompetenceFields(self):
            for competence in competence_field.getCompetences():
                competence_list.append(competence.to_dict(self))
        competence = dp.getEvaluationCompetence(self)
        competence_list.append(competence.to_dict(self))
        return competence_list

    def getQuestionResponses(self, respect_finished_at=None):
        """
        Get responses for questions
        """
        if respect_finished_at is None:
            respect_finished_at = True
        if self.finished_at is None and respect_finished_at:
            return None
        question_responses = list()

        for question in self.getDevelopmentPlan().getQuestions(self):
            question_response = self.getResponse(question.pk)
            question_responses.append({
                'text': '' if (question_response is None) else question_response,
                'pk': question.pk,
                'title': question.title
            })
        return question_responses

    def getResponse(self, question_id):
        """
        Get response for given question id
        """
        question_response = QuestionResponse.objects.filter(
            question__pk=question_id,
            development_plan_to_user_relation__pk=self.pk
        ).order_by('-client_timestamp', '-pk').first()
        if question_response:
            return question_response.text
        return None

    def getResponses(self):
        """
        Get all responses
        """
        return self.getQuestionResponses(False)

    def addResponse(self, question_id, text, timestamp, current_user):
        """
        Add a response for question with text for current user
        """

        question_response = QuestionResponse.objects.create(
            question=Question.objects.get(pk=question_id),
            client_timestamp=timestamp,
            development_plan_to_user_relation=self,
            text=text,
            created_by=current_user,
            updated_by=current_user
        )
        question_response.save()

    def markAsDone(self, current_user, is_private):
        """
        Mark the development plan as done and send notifications
        """
        if current_user != self.user:
            raise PermissionDenied()
        self.finished_at = datetime.datetime.now()
        self.is_private = is_private
        self.save()
        self._sendDoneNotifications()


    def _sendDoneNotifications(self):
        """
        Send notifications to employee/manager and receipt to self.user when done
        """
        language_code = self.getDevelopmentPlan().language_code
        if self.isManagers():
            template = loader.get_template('mus/emails/finished_manager_development_plan_%s.html' % language_code)
            if language_code == 'da':
                subject = "Din leder har udfyldt sin forberedelsesguide"
            elif language_code == 'en':
                subject = "Your manager has finished the preparation guide"
            else:
                raise PermissionDenied()
            htmlbody = template.render(
                Context({
                    'manager_user': self.user,
                    'user': self.getDevelopmentPlan().owner.user
                })
            )
            send_mail(
                subject,
                strip_tags(htmlbody),
                settings.DEFAULT_FROM_MAIL,
                ("%s <%s>" % (
                    self.getDevelopmentPlan().owner.user.get_full_name(), self.getDevelopmentPlan().owner.user.email),),
                html_message=htmlbody
            )
            template = loader.get_template('mus/emails/receipt_manager_development_plan_%s.html' % language_code)
            if language_code == 'da':
                subject = "Forberedelsesguide udfyldt for %s" % self.getDevelopmentPlan().owner.user.get_full_name()
            elif language_code == 'en':
                subject = "Preparation guide finished for %s" % self.getDevelopmentPlan().owner.user.get_full_name()
            else:
                raise PermissionDenied()
            htmlbody = template.render(
                Context({
                    'employee_user': self.getDevelopmentPlan().owner.user,
                    'user': self.user,
                })
            )
            send_mail(
                subject,
                strip_tags(htmlbody),
                settings.DEFAULT_FROM_MAIL,
                ("%s <%s>" % (self.user.get_full_name(), self.user.email),),
                html_message=htmlbody,
                attachment=[self.getPDFfile()]
            )
        else:
            template = loader.get_template('mus/emails/finished_employee_development_plan_%s.html' % language_code)
            if language_code == 'da':
                subject = "En medarbejder har udfyldt sin forberedelsesguide"
            elif language_code == 'en':
                subject = "An employee has finished the preparation guide"
            else:
                raise PermissionDenied()
            htmlbody = template.render(
                Context({
                    'employee_user': self.user,
                    'user': self.user.employee_user.first().manager.user
                })
            )
            send_mail(
                subject,
                strip_tags(htmlbody),
                settings.DEFAULT_FROM_MAIL,
                ("%s <%s>" % (self.user.employee_user.first().manager.user.get_full_name(),
                              self.user.employee_user.first().manager.user.email),),
                html_message=htmlbody
            )
            template = loader.get_template('mus/emails/receipt_employee_development_plan_%s.html' % language_code)
            if language_code == 'da':
                subject = "Din forberedelsesguide er udfyldt"
            elif language_code == 'en':
                subject = "Your preparation guide is finished"
            else:
                raise PermissionDenied()
            htmlbody = template.render(
                Context({
                    'user': self.user,
                })
            )
            send_mail(
                subject,
                strip_tags(htmlbody),
                settings.DEFAULT_FROM_MAIL,
                ("%s <%s>" % (self.user.get_full_name(), self.user.email),),
                html_message=htmlbody,
                attachment=[self.getPDFfile()]
            )


    def isMyMus(self):
        """
        Is it my development plan
        """
        try:
            return self.development_plan_manager.get().owner.user.pk == self.user.pk
        except DevelopmentPlan.DoesNotExist:
            return self.development_plan_employee.get().owner.user.pk == self.user.pk


    def toggleIsPrivate(self):
        """
        Toggle whether self is private
        """
        self.is_private = not self.is_private
        self.save()

    def getStatus(self):
        """
        Get status of self
        """
        if self.finished_at != None:
            return dict(number=2, description=_("Complete"))
        else:
            return dict(number=0, description=_("Incomplete"))


class DevelopmentPlanPageStatus(models.Model):
    pagelink = models.CharField(max_length=255, verbose_name=_(u'page link'))
    development_plan_relation = models.ForeignKey(DevelopmentPlanToUserRelation,
                                                  verbose_name=_('development plan relation'))
    UNREAD = 'UR'
    READ = 'RE'
    STATUS_CHOICES = (
        (UNREAD, _('Unread')),
        (READ, _('Read'))
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=UNREAD)

    class Meta:
        verbose_name = _(u'Development plan page status')
        verbose_name_plural = _(u'Development plan page statuses')


class DevelopmentPlan(models.Model):
    """
    An employee can only have one active development plan, and several completed
    """
    owner = models.ForeignKey(Employee, verbose_name=_(u"owner"))
    type = models.ForeignKey(DevelopmentPlanType, verbose_name=_(u'type'), null=True, blank=True)
    language_code = models.CharField(max_length=15, verbose_name=_(u'language'), choices=settings.LANGUAGES,
                                     default=settings.LANGUAGE_CODE)
    manager_response_relation = models.ForeignKey(
        DevelopmentPlanToUserRelation,
        verbose_name=_(u"manager response relation"),
        related_name='development_plan_manager'
    )
    employee_response_relation = models.ForeignKey(
        DevelopmentPlanToUserRelation,
        verbose_name=_(u"employee response relation"),
        related_name='development_plan_employee'
    )
    competence_fields = models.ManyToManyField(
        CompetenceField,
        verbose_name=_(u"competence fields"),
        related_name='development_plan_competence_fields'
    )
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='development_plan_created_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)
    deleted = models.BooleanField(verbose_name=_('deleted'), default=False)

    class Meta:
        verbose_name = _(u'development plan')
        verbose_name_plural = _(u'development plans')

    def __unicode__(self):
        return u'%s\'s development plan per %s' % (self.owner, self.created_at)

    def getLanguage(self):
        for language in settings.LANGUAGES:
            if language[0] == self.language_code:
                return language[1]

    def to_dict(self):
        """
        Convert to dictionary
        """
        return dict(
            id=self.pk,
            manager_response_relation=self.manager_response_relation.to_dict(),
            employee_response_relation=self.employee_response_relation.to_dict(),
        )

    def getAssignmentCompetence(self, development_plan_relation):
        """
        Get competence for assignment key for relation
        """
        return self.getFirstCompetenceFromCompetenceFieldId(development_plan_relation, 8)

    def getFirstCompetenceFromCompetenceFieldId(self, development_plan_relation, cfid):
        """
        Get first competence from given comptence field id for given relation
        """
        is_manager = development_plan_relation.pk == self.manager_response_relation.pk
        cf = CompetenceField.objects.filter(Q(pk=cfid) | Q(parent=cfid), language_code=self.language_code,
                                            development_plan_type=self.type, is_manager=is_manager)

        if cf:
            return cf[0].competence_competence_field.all()[0]
        cf = CompetenceField.objects.get(pk=cfid)
        if cf:
            return cf.competence_competence_field.all()[0]
        return None

    def getEvaluationCompetence(self, development_plan_relation):
        """
        Get evaluation competence for given relation
        """
        return self.getFirstCompetenceFromCompetenceFieldId(development_plan_relation, 7)

    def getCompetenceFields(self, development_plan_relation):
        """
        Get all non system competence fields for given relation
        """
        is_manager = development_plan_relation.pk == self.manager_response_relation.pk
        fields = list()
        for cf in self.competence_fields.order_by('sort_order'):
            cfs = CompetenceField.objects.filter(Q(pk=cf.pk) | Q(parent=cf.pk), language_code=self.language_code,
                                                 development_plan_type=self.type, is_manager=is_manager)
            if cfs:
                fields.append(cfs[0])
        return fields

    def getQuestions(self, development_plan_relation):
        """
        Get all related questions
        """
        questions = list()
        for question in self.getAssignmentCompetence(development_plan_relation).question_set.all().order_by(
                'sort_order'):
            questions.append(question)
        for competence_field in self.getCompetenceFields(development_plan_relation):
            for competence in competence_field.getCompetences():
                for question in competence.question_set.all().order_by('sort_order'):
                    questions.append(question)

        for question in self.getEvaluationCompetence(development_plan_relation).question_set.all().order_by(
                'sort_order'):
            questions.append(question)
        return questions

    def canManage(self, logged_user=None):
        """
        Is the logged in user a enso user, or manager in the company
        """

        if logged_user == None:
            logged_user = get_current_request().user

        if not logged_user.isEnsoUser():
            if not logged_user.isManager() or logged_user.company.pk != self.owner.company.pk:
                return False

        return True


class QuestionResponse(models.Model):
    """
    A response for a question
    """
    question = models.ForeignKey('Question', verbose_name=_(u"question"))
    development_plan_to_user_relation = models.ForeignKey(
        'DevelopmentPlanToUserRelation',
        verbose_name=_(u"development plan to user relation"),
        related_name='question_response_development_plan_to_user_relation'
    )
    text = models.TextField(verbose_name=_(u"text"), null=True)
    client_timestamp = models.BigIntegerField(verbose_name=_(u'client timestamp'), null=True)
    created_at = models.DateTimeField(verbose_name=_(u"created at"), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(u"created by"), related_name='question_response_created_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(verbose_name=_(u"updated at"), auto_now=True)
    updated_by = models.ForeignKey(User, verbose_name=_(u"updated by"), related_name='question_response_updated_by',
                                   blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'response')
        verbose_name_plural = _(u'responses')

    def __unicode__(self):
        return u'%s' % safeHtmlString(self.text, 100)


class FileBytes(models.Model):
    _data = models.TextField(db_column='data', blank=True)

    def set_data(self, data):
        self._data = base64.encodestring(data)

    def get_data(self):
        return base64.decodestring(self._data)

    data = property(get_data, set_data)


class File(models.Model):
    file_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField()
    file_path = models.FileField(upload_to='temp')
    file = models.ForeignKey(FileBytes, null=True, default=None, blank=True)
    company = models.ForeignKey(Company, related_name='files')
    role = models.ForeignKey(Role, related_name='files', null=True, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='file_created_by', blank=True, null=True,
                                   on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Fil'
        verbose_name_plural = u'Filer'

    def __unicode__(self):
        return u'%s' % safeHtmlString(self.file_name, 255)

    @staticmethod
    def getMyfiles(user):
        employee = Employee.objects.get(user=user)
        role_ids = employee.roles.values_list('employeerole__role__pk')
        return File.objects.filter(Q(role__pk__in=role_ids) | Q(role__pk=None))

    def canDownload(self, current_user):
        employee = Employee.objects.get(user=current_user)
        role_ids = employee.roles.values_list('employeerole__role__pk', flat=True)
        correct_company = employee.company == self.company
        has_needed_role = self.role is None
        if not has_needed_role:
            for role_id in role_ids:
                has_needed_role = has_needed_role or role_id == self.role.pk
        return correct_company and has_needed_role


class ReminderTemplate(models.Model):
    """
    Reminder Template model
    """

    ID_CONTRIBUTION_KEY = 1

    subject_en = models.CharField(max_length=255, null=True)
    subject_da = models.CharField(max_length=255, null=True)
    body_en = models.TextField(null=True)
    body_da = models.TextField(null=True)

    class Meta:
        verbose_name = 'Reminder Template'
        verbose_name_plural = 'Reminders Template'


    def __unicode__(self):
        return u'%s' % safeHtmlString(self.subject_en, 255)


class Reminder(models.Model):
    """
    Reminder model

    """

    created_by = models.ForeignKey(User, related_name='reminder_created_by', blank=False, null=False)
    """:type : User"""
    create_date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=255)
    template = models.ForeignKey(ReminderTemplate, related_name='reminder_template', blank=False, null=False)
    """:type : ReminderTemplate"""
    date = models.DateTimeField()
    send_date = models.DateTimeField()
    sent = models.DateTimeField(null=True)
    error = models.CharField(max_length=500, null=True)


    class Meta:
        verbose_name = 'Reminder'
        verbose_name_plural = 'Reminders'

    @staticmethod
    def getPending():
        """
        Get all reminders that needs to be sent

        :rtype: list[Reminder]
        """
        return Reminder.objects.filter(send_date__lte=now(), sent__isnull=True)


    def markSent(self):

        if self.sent is not None:
            raise Exception('Cannot mark as sent: Already sent at: {}'.format(self.sent))

        self.sent = now()
        self.save()


    def send(self):

        emp = Employee.objects.get(user=self.created_by)
        """:type Employee"""
        language_code = emp.language_code

        if language_code == 'da':
            subject = self.template.subject_da
            body = self.template.body_da
        else:
            subject = self.template.subject_en
            body = self.template.body_en

        message = html_message = body.format(
            self.created_by.get_full_name(),
            self.comment.replace('\n', '<br />\n')
        )

        send_mail(
            subject,
            strip_tags(message),
            settings.DEFAULT_FROM_MAIL,
            ("%s <%s>" % (self.created_by.get_full_name(), self.created_by.email),),
            html_message=message

        )

        self.markSent()

    @staticmethod
    def create(template_id, send_date, date, comment, created_by):
        """
        Create a new template object and persist.

        :rtype: Reminder
        """
        obj = Reminder()

        obj.template_id = template_id
        obj.send_date = send_date
        obj.date = date
        obj.comment = comment
        obj.created_by = created_by

        obj.create_date = now()
        obj.save()

        return obj


    def __unicode__(self):
        return u'Reminder(comment=%s, created_by=%s, created_date=%s, date=%s, send_date=%s, sent=%s)' % (
            safeHtmlString(self.comment, 255),
            self.created_by,
            self.create_date,
            self.date,
            self.send_date,
            self.sent
        )


