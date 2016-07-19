"""
Views for NXT LVL
"""
import StringIO
# from collections import OrderedDict
import os
# from pprint import pprint
from django.template.loader import get_template
import ho.pisa as pisa
from os import path
from django.views.decorators.cache import never_cache
from models import DevelopmentPlan, Competence, CompetenceField, Action, DevelopmentPlanType, DevelopmentPlanPageStatus
from common.util import csv_to_dict, LazyEncoder, logUnauthorizedAccess
from common.LeaderModel import LeaderModel
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
# from django.shortcuts import render_to_response
from models import Employee, File
from models import DevelopmentPlanToUserRelation, Company
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
# from django.template.loader import get_template
# from django.template import Context
from forms import EmployeeForm, EditEmployeeForm, AttachMUSForm, ActionForm, UploadEmployeesForm, \
    EmployeeRowFormSet, EmployeeManagerRowFormSet, EmployeeNoteForm, MultiLeaderModelForm, \
    UploadFileToEmployeyForm
from forms import ActionCommentForm, ChangeCompanyForm, PasswordResetForm
# from django.core.paginator import Paginator
from django.utils.encoding import smart_str
# from django.utils import timezone, translation
from django.db.models import Q
from django.utils.translation import ugettext as _, get_language
from django.contrib.auth import login
from django.template import Context
from django.core.exceptions import PermissionDenied
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
import common.util as util
import logging
from mimetypes import MimeTypes

logger = logging.getLogger(__name__)


@login_required
def clone_competencefields(request):
    cddtype = DevelopmentPlanType.objects.get(pk=3)
    for cf in CompetenceField.objects.filter(is_manager=False, language_code='da', development_plan_type__pk=1,
                                             company__isnull=True):
        cf.cloneTo(cddtype)
    for cf in CompetenceField.objects.filter(is_manager=True, language_code='da', development_plan_type__pk=1,
                                             company__isnull=True):
        cf.cloneTo(cddtype)
    return HttpResponse('done')


def start_view(request):
    """
    Decide where to go, dashboard if logged in, login form if not
    """

    if request.user and Employee.objects.filter(user__pk=request.user.pk).exists():
        if Employee.objects.get(user__pk=request.user.pk).is_manager:
            return HttpResponseRedirect('/dashboard')
        else:
            return HttpResponseRedirect('/employee/show/%d/' % request.user.employee_user.first().pk)
    else:
        return HttpResponseRedirect('/login/')


def accesscode(request, code):
    """
    Login with an accesscode
    """
    employee = Employee.objects.get(access_code=code)
    user = employee.user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return HttpResponseRedirect('/')


def password_reset(request):
    """
    Password reset view
    """
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/password_reset_done/')
    else:
        form = PasswordResetForm()
    return TemplateResponse(
        request,
        'reset.html',
        {
            'form': form,
            'next': '/password_reset_done/'
        }
    )


def password_reset_done(request):
    """
    Password reset done
    """

    return TemplateResponse(
        request,
        'reset_done.html',

    )


@login_required
@require_http_methods(['POST'])
def change_company(request):
    """
    Change company
    """
    employee = request.user.employee_user.first()
    if not employee.isEnsoUser() and employee.company.pk != request.POST['company']:
        raise PermissionDenied()
    return HttpResponseRedirect("/employee/all/%s" % request.POST['company'])


@login_required
def developmentplan_mark_link_as_read(request):
    """
    Mark a point in the development plan as read
    """
    data = json.loads(request.body)
    development_plan_user_id = data['development_plan_user_id']
    link = data['link']
    dpr = DevelopmentPlanToUserRelation.objects.get(pk=int(development_plan_user_id))
    DevelopmentPlanPageStatus.objects.get_or_create(development_plan_relation=dpr, pagelink=link,
                                                    status=DevelopmentPlanPageStatus.READ)
    return HttpResponse('OK')


@login_required
def remove_development_plan(request, development_plan_id):
    """
    Remove development plan
    """
    dp = DevelopmentPlan.objects.get(pk=development_plan_id)
    employee = request.user.employee_user.first()
    if not employee.isEnsoUser() and employee.company.pk != dp.owner.company.pk:
        raise PermissionDenied()
    dp.deleted = True
    dp.owner.newest_development_plan = None
    dp.owner.save()
    dp.save()
    return HttpResponseRedirect('/employee/all/%d' % dp.owner.company.pk)


@login_required
def reopen_development_plan(request, development_plan_id, is_managers):
    """
    Reopen development plan
    """

    dp = DevelopmentPlan.objects.get(pk=development_plan_id)
    """:type : DevelopmentPlan """
    logged_user = request.user.employee_user.first()
    """:type : Employee """

    if not dp.canManage(logged_user):
        raise PermissionDenied()

    if is_managers == 'true':
        dp.manager_response_relation.finished_at = None
        dp.manager_response_relation.is_private = 0
        dp.manager_response_relation.save()
    else:
        dp.employee_response_relation.finished_at = None
        dp.employee_response_relation.is_private = 0
        dp.employee_response_relation.save()

    return HttpResponseRedirect('/employee/show/{}/'.format(dp.owner.id))


@login_required
def development_plan(request, development_plan_user_id=None):
    """
    Display development plan for edit
    """
    if not development_plan_user_id:
        employee = Employee.objects.get(user=request.user)
        devplan = employee.getDevelopmentPlans().first()
        if devplan:
            development_plan_user = devplan.employee_response_relation
        else:
            return HttpResponse('unauthorized', status=401)
    else:
        development_plan_user = DevelopmentPlanToUserRelation.objects.get(pk=int(development_plan_user_id))
        if development_plan_user.is_private and development_plan_user.user.pk != request.user.pk:
            return HttpResponse('unauthorized', status=401)
    return TemplateResponse(
        request,
        'mus/development_plan.html',
        {
            'development_plan_user': development_plan_user,
        }
    )


@login_required
def development_plan_receipt(request, development_plan_user_id):
    """
    Display receipt after completing development plan
    """
    development_plan_user = DevelopmentPlanToUserRelation.objects.get(pk=int(development_plan_user_id))
    if development_plan_user.user.pk != request.user.pk:
        raise PermissionDenied()
    return TemplateResponse(
        request,
        'mus/development_plan_receipt.html',
        {
            'development_plan_user': development_plan_user,
        }
    )


@login_required
def development_plan_html(request, development_plan_user_id):
    development_plan_user = DevelopmentPlanToUserRelation.objects.get(pk=int(development_plan_user_id))
    devplan = development_plan_user.getDevelopmentPlan()
    return TemplateResponse(
        request,
        'mus/development_plan_pdf.html',
        {
            'company': devplan.owner.company,
            'owner_name': devplan.owner,
            'extension': "%s_%s%s" % (devplan.language_code.lower(), devplan.type.name.lower()[:-3],
                                      development_plan_user.isManagers() and "_manager" or ""),
            'development_plan_user': development_plan_user,
            'assignment_competence': devplan.getAssignmentCompetence(development_plan_user),
            'evaluation_competence': devplan.getEvaluationCompetence(development_plan_user),
            'competence_fields': devplan.getCompetenceFields(development_plan_user),
        }
    )


@login_required
def development_plan_pdf(request, development_plan_user_id):
    """
    Display development plan relation as pdf
    """
    development_plan_user = DevelopmentPlanToUserRelation.objects.get(pk=int(development_plan_user_id))

    employee = request.user.employee_user.first()
    if (development_plan_user.is_private and development_plan_user.user.pk != request.user.pk) or (
                not employee.isEnsoUser() and employee.company.pk != development_plan_user.getDevelopmentPlan().owner.company.pk):
        raise PermissionDenied()
    with open(development_plan_user.getPDFfile()) as pdf:
        response = HttpResponse(pdf.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline;filename=%s %s.pdf' % (
            "preparation guide", development_plan_user.user.get_full_name())
        return response


@login_required
@require_http_methods(['POST'])
def finish_development_plan(request):
    """
    Finish development plan and send notifications
    """
    data = json.loads(request.body)
    development_plan_user = DevelopmentPlanToUserRelation.objects.get(pk=data['development_plan_user_id'])
    if development_plan_user.user.pk != request.user.pk:
        return HttpResponse('unauthorized', status=401)
    development_plan_user.markAsDone(request.user, data['is_private'])
    response = json.dumps(dict(redirectUrl='/developmentplan/' + str(development_plan_user.pk) + '/receipt'))

    return HttpResponse(response, content_type='application/json')


@login_required
def get_development_plan(request, development_plan_user_id):
    """
    Get development plan as json
    """
    development_plan_user = DevelopmentPlanToUserRelation.objects.get(pk=int(development_plan_user_id))
    if development_plan_user.user.pk != request.user.pk:
        return HttpResponse('unauthorized', status=401)
    response = json.dumps(development_plan_user.getCompetencesAsDict())
    return HttpResponse(response, content_type='application/json')


@login_required
@never_cache
def get_development_plan_states(request, development_plan_user_id):
    """
    Get states of development plan relation as json
    """
    development_plan_user = DevelopmentPlanToUserRelation.objects.get(pk=int(development_plan_user_id))
    if development_plan_user.user.pk != request.user.pk:
        return HttpResponse('unauthorized', status=401)
    response = json.dumps(development_plan_user.getStates(), cls=LazyEncoder)
    return HttpResponse(response, content_type='application/json')


@login_required
@never_cache
def get_development_plan_competence(request, development_plan_user_id, competence_id):
    """
    Get competence of development plan relation as json
    """
    development_plan_user = DevelopmentPlanToUserRelation.objects.get(pk=int(development_plan_user_id))
    if development_plan_user.user.pk != request.user.pk:
        return HttpResponse('unauthorized', status=401)
    competence = Competence.objects.get(pk=int(competence_id))
    c = competence.to_dict(development_plan_user)
    response = json.dumps(c)
    return HttpResponse(response, content_type='application/json')


@login_required
@never_cache
def get_development_plan_competence_field(request, development_plan_user_id, competence_field_id):
    """
    Get competence field for development plan relation as json
    """
    development_plan_user = DevelopmentPlanToUserRelation.objects.get(pk=int(development_plan_user_id))
    if development_plan_user.user.pk != request.user.pk:
        return HttpResponse('unauthorized', status=401)
    competence_field = CompetenceField.objects.get(pk=int(competence_field_id))
    response = json.dumps(competence_field.to_dict())
    return HttpResponse(response, content_type='application/json')


@login_required
@require_http_methods(['POST'])
def save_development_plan_question(request, development_plan_user_id, question_id):
    """
    Save development plan relation question response
    """
    if 'response' in request.POST:
        response = request.POST['response']
        timestamp = 2
    else:
        data = json.loads(request.body)
        response = data['response']
        timestamp = data['timestamp']

    development_plan_user = DevelopmentPlanToUserRelation.objects.get(pk=int(development_plan_user_id))
    if not request.user == development_plan_user.user or development_plan_user.finished_at:
        return HttpResponse('unauthorized', status=401)

    development_plan_user.addResponse(int(question_id), response, timestamp, request.user)
    return HttpResponse('')


@login_required
def attach_development_plan(request, company_id):
    """
    View for attach development plan to employees
    """
    company = Company.objects.get(pk=company_id)
    employee = Employee.objects.get(user__pk=request.user.pk)
    if not employee.isEnsoUser() and employee.company.pk != company.pk:
        raise PermissionDenied()

    if employee.isCompanySuperUserOrHigher():

        employeeQS = Employee.objects.filter(

            Q(newest_development_plan__isnull=True) |
            Q(
                Q(newest_development_plan__isnull=False) &
                Q(newest_development_plan__manager_response_relation__finished_at__isnull=False) &
                Q(newest_development_plan__employee_response_relation__finished_at__isnull=False)
            ),
            company__pk=company_id

        ).distinct()
    else:

        employeeQS = Employee.objects.filter(
            # First employee must be attached to a manager, either directly, or 3 levels down
            Q(manager=employee) |
            Q(manager__manager=employee) |
            Q(manager__manager__manager=employee) |
            Q(manager__manager__manager__manager=employee),  # AND
            Q(newest_development_plan__isnull=True) |  # OR
            Q(
                Q(newest_development_plan__isnull=False) &
                Q(newest_development_plan__manager_response_relation__finished_at__isnull=False) &
                Q(newest_development_plan__employee_response_relation__finished_at__isnull=False)
            ),
            company__pk=company_id

        ).distinct()

    if request.method == 'POST':
        form = AttachMUSForm(request.POST)
        form.fields['employees'].queryset = employeeQS
        if form.is_valid():
            employees = form.cleaned_data['employees']
            email_text = form.cleaned_data['email_text']
            competence_fields = form.cleaned_data['competence_fields']
            template_code = form.cleaned_data['template']
            for employee in employees:
                employee.createDevelopmentPlan(competence_fields, request.user, email_text, template_code)
            return HttpResponseRedirect('/employee/all/%d' % int(company_id))
    else:
        form = AttachMUSForm()
        form.fields['employees'].queryset = employeeQS
    cfs = CompetenceField.objects.filter(Q(company=None) | Q(company__pk=company.pk), parent=None,
                                         is_system=False).order_by('sort_order')

    colors = ['#dfc93f', '#f05e38', '#dc4050', '#34bead', '#268376', '#053e38', '#0bb3e2', '#0890b6', '#1e74a3']
    cf_list = list()
    language_code = get_language()
    for i, cf in enumerate(cfs):
        field = CompetenceField.objects.filter(Q(pk=cf.pk) | Q(parent=cf.pk), language_code=language_code).first()
        cf_list.append(dict(color=colors[i], field=field))
    matrix = list()
    matrix.append(cf_list[:3])
    cf_list = cf_list[3:]
    matrix.append(cf_list[:3])
    cf_list = cf_list[3:]
    matrix.append(cf_list[:3])
    # cf_list = cf_list[3:]

    return TemplateResponse(
        request,
        'mus/attach_development_plan.html',
        {
            'form': form,
            'company': company,
            'competence_fields': matrix,
            'colors': colors
        }
    )


@login_required
def all_employees(request, company_id=None):
    """
    View for all employees (in company) or for current user dependent on employee role
    """
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    company_super_user = current_employee.isCompanySuperUserOrHigher()
    if company_id:
        company = Company.objects.get(pk=company_id)
    else:
        company = current_employee.company
    if not current_employee.isEnsoUser() and current_employee.company.pk != company.pk:
        raise PermissionDenied()
    change_company_form = ChangeCompanyForm(initial=dict(company=company))
    return TemplateResponse(
        request,
        'mus/all_employees.html',
        {
            'user': request.user,
            'company_super_user': company_super_user,
            'company': company,
            'change_company_form': change_company_form,
        }
    )


@login_required
@never_cache
def employees_json(request, company_id=None):
    """
    Get all employees as json
    """
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    # questionnaire_companies = currnet_employee.company.getAvailableSchemes()
    company_super_user = current_employee.isCompanySuperUserOrHigher()
    if company_id:
        company = Company.objects.get(pk=company_id)
    else:
        company = current_employee.company
    if not current_employee.isEnsoUser() and current_employee.company.pk != company.pk:
        raise PermissionDenied()
    if company_super_user:
        managers = company.getTopManagers()
    else:
        managers = list()
        managers.append(current_employee)
    employees = list()
    for manager in managers:
        employees.append(manager.to_dict())
    response = json.dumps(employees, cls=LazyEncoder)
    return HttpResponse(response, content_type='application/json')


@login_required
@require_http_methods(['POST'])
def add_employee(request):
    """
    Add employee
    """
    form = EmployeeForm(request, request.POST or None)
    if not form.is_valid():
        return TemplateResponse(request, 'mus/create_employee_form.html', {'employee_form': form})
    form.save()
    return HttpResponseRedirect('/employee/all/%d' % form.cleaned_data.get('company').pk)


def employee_delete_file(request, employee_id, filename):
    """
    Securely download files from user.

    :param request: HttpRequest
    :param employee_id: int
    :param filename: str
    :return:
    """

    current_user = Employee.objects.get(user__pk=request.user.pk)

    if not current_user.hasAccessTo(employee_id):
        logUnauthorizedAccess(
            "User tried to delete file he didnt have access to", request, filename
        )
        return HttpResponse('unauthorized', status=401)

    user_dir = util.get_user_files_dir(employee_id)
    filename = os.path.join(user_dir, filename.replace('..', ''))

    if not os.path.isfile(filename):
        return HttpResponseNotFound('File does not exist')

    os.remove(filename)

    return HttpResponseRedirect(reverse('employee_detail', args=[employee_id]))


def employee_download_file(request, employee_id, filename):
    """
    Securely download files from user.

    :param request: HttpRequest
    :param employee_id: int
    :param filename: str
    :return:
    """

    current_user = Employee.objects.get(user__pk=request.user.pk)

    if not current_user.hasAccessTo(employee_id):
        logUnauthorizedAccess(
            "User tried to download file he didnt have access to", request, filename
        )
        return HttpResponse('unauthorized', status=401)

    user_dir = util.get_user_files_dir(employee_id)
    filename = os.path.join(user_dir, filename.replace('..', ''))

    if not os.path.isfile(filename):
        return HttpResponseNotFound('File does not exist')

    wrapper = FileWrapper(file(filename))

    ext = os.path.splitext(filename)[1].lower()

    response = HttpResponse(
        wrapper,  # i'd rather do this hack than use urllib.pathname2url
        content_type=MimeTypes().guess_type('/bogus/path/bogus_file' + ext)
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    response['Content-Length'] = os.path.getsize(filename)

    return response


def get_files_for_employee(employee_id):
    """

    :param employee_id: int
    :return: list[str]
    """

    user_dir = util.get_user_files_dir(employee_id)

    return [f for f in os.listdir(user_dir) if os.path.isfile(os.path.join(user_dir, f))]


@login_required
def employee_detail(request, employee_id):
    """
    View for detail of employee
    """
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    employee = Employee.objects.get(pk=int(employee_id))
    if not current_employee.isEnsoUser() and current_employee.company.pk != employee.company.pk:
        raise PermissionDenied()
    development_plans = employee.getDevelopmentPlans()
    actions = employee.action_set.all()
    if not current_employee.pk == int(employee_id):
        if not current_employee.is_manager or not current_employee.company.pk == employee.company.pk:
            if not current_employee.isCompanySuperUserOrHigher():
                return HttpResponse('unauthorized', status=401)

    user_files = get_files_for_employee(employee_id)

    if request.method == 'POST':

        upload_form = UploadFileToEmployeyForm(request.POST, request.FILES)
        form = EmployeeNoteForm(request.POST, instance=employee)

        if 'upload' in request.POST:
            if upload_form.is_valid():
                upload_form.handle_upload(employee_id, request.FILES['file'])

                return HttpResponseRedirect('/employee/show/{}?upload_status=ok#file-list'.format(employee_id))

        else:
            if form.is_valid():
                form.save(request.user, employee)
                return HttpResponseRedirect('/employee/show/%d' % form.instance.pk)

    else:
        form = EmployeeNoteForm(instance=employee)
        upload_form = UploadFileToEmployeyForm()

    return TemplateResponse(
        request,
        'mus/detail.html',
        {
            'actions': actions,
            'employee': employee,
            'development_plans': development_plans,
            'form': form,
            'upload_form': upload_form,
            'user_files': user_files
        }
    )


@login_required
def create_employee(request, company_id):
    """
    View for creating employee in company
    """
    company = Company.objects.get(pk=company_id)
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    if not current_employee.isEnsoUser() and current_employee.company.pk != company.pk:
        logUnauthorizedAccess("User tried to create_employee", request)
        raise PermissionDenied()
    form = EmployeeForm(request, initial=dict(company=company))
    form.fields['manager'].queryset = Employee.objects.filter(is_manager=True, company=company)
    form.fields['development_plan_type'].queryset = DevelopmentPlanType.objects.filter(
        Q(company=company) | Q(company__isnull=True))
    return TemplateResponse(
        request,
        'mus/create_employee_form.html',
        {
            'employee_form': form,
            'company': company
        }
    )


@login_required
def create_many_employees(request, company_id=None):
    """
    View for creating many employees in company
    """
    company = Company.objects.get(pk=company_id)
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    if not current_employee.isEnsoUser() and current_employee.company.pk != company.pk:
        raise PermissionDenied()
    if "upload" in request.POST:
        form = UploadEmployeesForm(request.POST, request.FILES)
        if form.is_valid():
            data = csv_to_dict(request.FILES['file'])
            request.session['upload_employees'] = data
            return TemplateResponse(
                request,
                'mus/create_many_employees_uploaded.html',
                dict(data=data, company=company)
            )
    elif "next" in request.POST:
        data = request.session['upload_employees']
        marked_data = list()
        fields = request.POST.getlist('field[]')
        for row in data:
            new_row = dict(is_manager=False)
            for i, item in enumerate(row):
                field_id = int(fields[i])
                if field_id == 1:
                    new_row['first_name'] = item
                elif field_id == 2:
                    new_row['last_name'] = item
                elif field_id == 3:
                    p = item.partition(" ")
                    new_row['first_name'] = p[0]
                    new_row['last_name'] = p[2]
                elif field_id == 4:
                    new_row['email'] = item
                elif field_id == 5:
                    new_row['username'] = item
            marked_data.append(new_row)
        formset = EmployeeRowFormSet(initial=marked_data)
        TypeQS = DevelopmentPlanType.objects.filter(Q(company=company) | Q(company__isnull=True))
        for form in formset:
            form.fields['development_plan_type'].queryset = TypeQS
        return TemplateResponse(
            request,
            'mus/create_many_employees_form.html',
            dict(formset=formset, company=company)
        )
    elif "next2" in request.POST:
        formset = EmployeeRowFormSet(request.POST)
        if formset.is_valid():
            data = list()

            for i, form in enumerate(formset):
                data.append(dict(employee=form.save(request.user, company)))
            newformset = EmployeeManagerRowFormSet(initial=data)
            managerQS = Employee.objects.filter(is_manager=True, company__pk=company.pk)
            for form in newformset:
                form.fields['manager'].queryset = managerQS
            return TemplateResponse(
                request,
                'mus/create_many_employees_manager.html',
                dict(formset=newformset, company=company)
            )
        else:
            return TemplateResponse(
                request,
                'mus/create_many_employees_form.html',
                dict(formset=formset, company=company)
            )
    elif "next3" in request.POST:
        formset = EmployeeManagerRowFormSet(request.POST)
        managerQS = Employee.objects.filter(is_manager=True, company__pk=company.pk)
        for form in formset:
            form.fields['manager'].queryset = managerQS
        if formset.is_valid():
            for form in formset:
                form.save(request.user)

            return HttpResponseRedirect('/employee/all/%d' % company.pk)
        else:
            return TemplateResponse(
                request,
                'mus/create_many_employees_manager.html',
                dict(formset=formset, company=company)
            )
    form = UploadEmployeesForm()
    return TemplateResponse(
        request,
        'mus/create_many_employees.html',
        dict(form=form, company=company))


@login_required
@require_http_methods(['POST'])
def update_employee(request, employee_id):
    """
    Update employee
    """
    employee = Employee.objects.get(pk=int(employee_id))
    current_employee = Employee.objects.get(user__pk=request.user.pk)
    if not current_employee.isEnsoUser() and current_employee.company.pk != employee.company.pk:
        raise PermissionDenied()
    form = EditEmployeeForm(request.user, employee, request.POST or None)
    if 'manager' in form.fields:
        managerQS = Employee.objects.filter(is_manager=True, company__pk=employee.company.pk)
        form.fields['manager'].queryset = managerQS
    if not form.is_valid():
        is_me = employee.user.pk == request.user.pk
        return TemplateResponse(
            request,
            'mus/edit_employee_form.html',
            {
                'edit_employee_form': form,
                'employee_id': employee_id,
                'me': is_me,
                'name': employee.user.get_full_name()
            }
        )
    form.save()
    return HttpResponseRedirect('/employee/show/' + employee_id + '/')


@login_required
def edit_employee(request, employee_id):
    """
    View for editing employee
    """
    employee = Employee.objects.get(pk=int(employee_id))
    current_employee = Employee.objects.get(user__pk=request.user.pk)

    assert isinstance(employee, Employee)
    assert isinstance(current_employee, Employee)

    # if not current_employee.isEnsoUser() and current_employee.company.pk != employee.company.pk:
    # raise PermissionDenied()

    if not current_employee.hasAccessTo(employee):
        raise PermissionDenied()

    form = EditEmployeeForm(request.user, employee, {
        'first_name': employee.user.first_name,
        'last_name': employee.user.last_name,
        'email': employee.user.email,
        'manager': employee.manager.id if employee.manager else 0,
        'language_code': employee.language_code,
        'development_plan_type': employee.development_plan_type.id,
        'is_manager': employee.is_manager
    })
    if 'manager' in form.fields:
        managerQS = Employee.objects.filter(is_manager=True, company__pk=employee.company.pk)
        form.fields['manager'].queryset = managerQS
        form.fields['development_plan_type'].queryset = DevelopmentPlanType.objects.filter(
            Q(company__pk=employee.company.pk) | Q(company__isnull=True)
        )
    is_me = employee.user.pk == request.user.pk
    return TemplateResponse(
        request,
        'mus/edit_employee_form.html',
        {
            'edit_employee_form': form,
            'employee_id': employee_id,
            'me': is_me,
            'name': employee.user.get_full_name()
        }
    )


@login_required
def files(request):
    fs = File.getMyfiles(request.user)
    return TemplateResponse(
        request,
        'mus/files.html',
        {
            'files': fs
        }
    )


@login_required
def get_file(request, file_id):
    f = File.objects.get(pk=int(file_id))
    if not f.canDownload(request.user):
        return HttpResponse('unauthorized', status=401)
    response = HttpResponse(
        f.file.data,
        mimetype=f.mime_type
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(f.file_name)
    response['Content-Length'] = smart_str(f.file_size)
    return response


@login_required
def dashboard(request):
    """
    View of dashboard containing overview of relevant information
    """
    employee = request.user.employee_user.first()
    widgets = list()
    development_plans = employee.getDevelopmentPlans()
    if employee.is_manager:
        widgets.append(dict(
            template="mus/_widget_waiting_developmentplans.html",
            data=employee.getMyEmployees(),
            title=_('Expecting preparation guides from')
        ))
        widgets.append(dict(
            template="mus/_widget_todo_developmentplans.html",
            data=employee.getMyEmployees(),
            title=_('Preparation guides to do')
        ))
    # widgets.append(dict(
    #        template = "mus/_widget_my_developmentplans.html",
    #        data = development_plans,
    #        title = _('My development plans')
    #    ))
    return TemplateResponse(
        request,
        'mus/dashboard.html',
        {
            'widgets': widgets,
            'employee': employee,
            'development_plans': development_plans
        })


@login_required
def action_list(request, employee_id=None):
    """
    View for list of actions of (current) employee
    """
    if employee_id:
        employee = Employee.objects.get(pk=employee_id)
        current_employee = Employee.objects.get(user__pk=request.user.pk)
        if not current_employee.isEnsoUser() and current_employee.company.pk != employee.company.pk:
            raise PermissionDenied()
    else:
        employee = request.user.employee_user.first()
    actions = employee.action_set.all()
    return TemplateResponse(
        request,
        'mus/action_list.html',
        dict(
            actions=actions,
            employee=employee
        )
    )


@login_required
def action_edit(request, action_id):
    """
    View for editing action
    """
    employee = request.user.employee_user.first()
    action = Action.objects.get(pk=action_id)
    if not employee.isEnsoUser() and employee.company.pk != action.employee.company.pk:
        raise PermissionDenied()
    if request.method == 'POST':
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            form.save(request.user, employee)
            return HttpResponseRedirect('/action/%d' % form.instance.pk)
    else:
        form = ActionForm(instance=action)
    return TemplateResponse(
        request,
        'mus/action_edit.html',
        dict(
            form=form,
            edit=True
        )
    )


@login_required
def action_detail(request, action_id):
    """
    View for detail of action
    """
    employee = request.user.employee_user.first()
    action = Action.objects.get(pk=int(action_id))
    # if not employee.isEnsoUser() and employee.company.pk != action.employee.company.pk:
    if not employee.hasAccessTo(action.employee):
        raise PermissionDenied()

    if request.method == 'POST':
        form = ActionCommentForm(request.POST)
        if form.is_valid():
            form.save(request.user, action)
            return HttpResponseRedirect('/action/%s' % action_id)
    else:
        form = ActionCommentForm()
    return TemplateResponse(
        request,
        'mus/action_detail.html',
        dict(
            action=action,
            form=form
        )
    )


@login_required
def action_add(request, employee_id=None):
    """
    View for creating action
    """
    if employee_id:
        employee = Employee.objects.get(pk=employee_id)
        current_employee = Employee.objects.get(user__pk=request.user.pk)
        if not current_employee.isEnsoUser() and current_employee.company.pk != employee.company.pk:
            raise PermissionDenied()
    else:
        employee = request.user.employee_user.first()
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            form.save(request.user, employee)
            return HttpResponseRedirect('/action/%d' % form.instance.pk)
    else:
        form = ActionForm()
    return TemplateResponse(
        request,
        'mus/action_edit.html',
        dict(
            form=form
        )
    )


@login_required
def create_leader_model(request, company_id):
    """
    Create a leader model for employees
    """

    errors = {'noactions': []}
    company = Company.objects.get(pk=company_id)
    currentEmpl = Employee.objects.get(user__pk=request.user.pk)
    """:type : Employee """

    if not currentEmpl.isEnsoUser() and currentEmpl.company.pk != company.pk:
        raise PermissionDenied()

    if currentEmpl.isCompanySuperUserOrHigher():
        employeeQS = Employee.objects.filter(
            company__pk=company_id
        )
    else:
        employeeQS = Employee.objects.filter(
            Q(manager=currentEmpl),
            company__pk=company_id
        )

    form = MultiLeaderModelForm(request.POST or None)
    form.fields['employees'].queryset = employeeQS

    if request.method == 'POST' and form.is_valid():

        employees = form.cleaned_data['employees']
        """:type : list[Employee] """

        pdf_response = get_leader_model_pdf(currentEmpl, employees)

        if isinstance(pdf_response, HttpResponse):
            return pdf_response
        else:
            errors = pdf_response

    print(errors)

    return TemplateResponse(
        request,
        'mus/create_leader_model.html', {
            'form': form,
            'company': company,
            'errors': errors
        }
    )


def get_leader_model_pdf(currentEmpl, employees):
    """
    Create LeaderModel and send it as a PDF to the browser

    :param currentEmpl: Employee
    :param employees: list[Employee]
    :return:
    """

    lm = LeaderModel()
    employee_actions = {}
    legend = []
    colors = {}
    errors = {'noactions': []}
    # numbered_actions = {}

    for empl in employees:

        if not currentEmpl.hasAccessTo(empl):
            raise PermissionDenied()

        actions = empl.action_set.all()

        if not len(actions):
            errors['noactions'].append(empl)
            continue

        lkey = empl.user.first_name + " " + empl.user.last_name
        legend.append(lkey)

        if not lkey in employee_actions:
            employee_actions[lkey] = {}

        for action in actions:

            if not action.difficulty or not action.type:
                errors['noactions'].append(empl)
                continue

            circle_number = lm.addCircle(action)
            latest_comment = action.getLatestComment()

            employee_actions[lkey][circle_number] = {
                'name': action.title,
                'type': action.type,
                'difficulty': action.getDifficultyText(),
                'comment': latest_comment
            }

            if lkey not in colors:
                color = lm.getEmployeeColors(empl.id)
                colors[lkey] = "rgb({}, {}, {})".format(color[0], color[1], color[2])

    if len(errors['noactions']):
        return errors

    lm_filename = path.join(settings.STATIC_ROOT, "leadermodel_{}.png".format(currentEmpl.id))
    lm.writeImage(lm_filename)

    #
    # Write PDF

    pdfFilename = path.join(settings.FILES_ROOT, "leadermodel_{}.pdf".format(currentEmpl.id))
    template = get_template('mus/leader_model_pdf.html')
    context = Context({
        'site_url': settings.SITE_URL,
        'lm_filename': lm_filename,
        'employee_actions': employee_actions,
        'colors': colors,
        'legend': legend
    })

    html = template.render(context)
    # html = html.replace('<li>','<li><img class="square" src="http://test.nxtlvl.dk/static/img/square.png" />')
    result = open(pdfFilename, 'wb')
    pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), dest=result)
    result.close()

    wrapper = FileWrapper(file(pdfFilename))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename=ledermodel.pdf'
    response['Content-Length'] = os.path.getsize(pdfFilename)

    return response
    # return HttpResponseRedirect('/employee/all/%d' % int(company_id))