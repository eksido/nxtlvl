from django.conf.urls import patterns, include, url
from ensomus.apps.mus.views import add_employee, employee_detail, update_employee, \
	employee_delete_file
from ensomus.apps.mus.views import employees_json, create_employee, edit_employee, all_employees, attach_development_plan, create_many_employees
from ensomus.apps.mus.views import files, get_file
from ensomus.apps.mus.views import development_plan,get_development_plan, get_development_plan_states, get_development_plan_competence
from ensomus.apps.mus.views import get_development_plan_competence_field, finish_development_plan,development_plan_receipt, development_plan_pdf,development_plan_html, reopen_development_plan
from ensomus.apps.mus.views import save_development_plan_question, remove_development_plan, developmentplan_mark_link_as_read
from ensomus.apps.mus.views import action_list, action_detail,action_add, action_edit
from ensomus.apps.mus.views import dashboard,start_view, change_company,accesscode, password_reset,password_reset_done, clone_competencefields
from ensomus.apps.mus.views import create_leader_model, employee_download_file

from django.contrib.auth import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'ensomus.views.home', name='home'),
	# url(r'^ensomus/', include('ensomus.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^clone$',clone_competencefields),
	url(r'^accesscode/(?P<code>\w+)$', accesscode),
	url(r'^employee/all/$', all_employees),
	url(r'^employee/all/(?P<company_id>\d+)$', all_employees),
	url(r'^employee/changecompany$', change_company),
	url(r'^employee/add/$', add_employee),
	url(r'^employee/json/(?P<company_id>\d+)$', employees_json),
	url(r'^employee/create/(?P<company_id>\d+)$', create_employee),
	url(r'^employee/create-many/(?P<company_id>\d+)$', create_many_employees),
	url(r'^employee/edit/(?P<employee_id>\d+)/$', edit_employee),
	url(r'^employee/attach/(?P<company_id>\d+)$', attach_development_plan),
	url(r'^employee/update/(?P<employee_id>\d+)/$', update_employee, name = 'update_employee'),
	url(r'^employee/show/(?P<employee_id>\d+)/$', employee_detail, name='employee_detail'),
	url(r'^employee/createleadermodel/(?P<company_id>\d+)$', create_leader_model),
	url(r'^employee/download-file/(?P<employee_id>\d+)/(?P<filename>.+)$', employee_download_file, name="employee_download_file"),
	url(r'^employee/delete-file/(?P<employee_id>\d+)/(?P<filename>.+)$', employee_delete_file, name="employee_delete_file"),
	url(r'^action/list/(?P<employee_id>\d+)$', action_list),
	url(r'^action/all$', action_list),
	url(r'^action/(?P<action_id>\d+)$', action_detail),
	url(r'^action/edit/(?P<action_id>\d+)$', action_edit),
	url(r'^action/add/(?P<employee_id>\d+)$', action_add),
	url(r'^dashboard$', dashboard),
	url(r'^developmentplan/$', development_plan),
	url(r'^developmentplan/finish/$', finish_development_plan),
	url(r'^developmentplan/mark-link-as-read/$', developmentplan_mark_link_as_read),
	url(r'^developmentplan/(?P<development_plan_id>\d+)/reopen/(?P<is_managers>\w*)$', reopen_development_plan),
	url(r'^developmentplan/(?P<development_plan_id>\d+)/remove$', remove_development_plan),
	url(r'^developmentplan/(?P<development_plan_user_id>\d+)/receipt$', development_plan_receipt),
	url(r'^developmentplan/(?P<development_plan_user_id>\d+)/pdf$', development_plan_pdf),
	url(r'^developmentplan/(?P<development_plan_user_id>\d+)/html$', development_plan_html),
	url(r'^developmentplan/(?P<development_plan_user_id>\d+)$', development_plan),
	url(r'^developmentplan/get/(?P<development_plan_user_id>\d+)$', get_development_plan),
	url(r'^developmentplan/save/(?P<development_plan_user_id>\d+)/(?P<question_id>\d+)$', save_development_plan_question),
	url(r'^developmentplan/get-states/(?P<development_plan_user_id>\d+)$', get_development_plan_states),
	url(r'^developmentplan/get-competence/(?P<development_plan_user_id>\d+)/(?P<competence_id>\d+)$', get_development_plan_competence),
	url(r'^developmentplan/get-competence-field/(?P<development_plan_user_id>\d+)/(?P<competence_field_id>\d+)$', get_development_plan_competence_field),
	url(r'^files/$', files),
	url(r'^files/get/(?P<file_id>\d+)/$', get_file),
	url(r'^$', start_view),
	url(r'^login/$', views.login, {'template_name': 'login.html'}),
	url(r'^logout/$', views.logout, {'next_page': '/'}),
	url(r'^password_reset/$', password_reset),
	url(r'^password_reset_done/$', password_reset_done),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^tinymce/', include('tinymce.urls')),
	url(r'^i18n/',include('django.conf.urls.i18n')),
)
