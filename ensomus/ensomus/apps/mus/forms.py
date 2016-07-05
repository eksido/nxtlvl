"""
Forms for NXT LVL
"""
from django import forms
from django_mailer_plus import send_mail
from models import Employee, CompetenceField,Action,DevelopmentPlanType, ActionComment, Company, Reminder, ReminderTemplate
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.template import loader, Context
from django.forms.formsets import formset_factory,BaseFormSet
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.db.models import Q
import widgets
from django.utils.html import strip_tags
from common.util import my_encrypt, generate_password, logUnauthorizedAccess
import os
from django.utils.timezone import now, utc
from datetime import date, datetime, time
import logging
import common.util as util
from threadlocals.threadlocals import get_current_request

logger = logging.getLogger(__name__)

class PasswordResetForm(forms.Form):
	"""
	Form to reset password and send the new password by mail
	"""
	email = forms.EmailField(label=_("Email"))
	def save(self):
		employee = Employee.objects.get(user__email__exact=self.cleaned_data['email'])
		subject = _("NXT LVL: new password")
		password = generate_password(8)
		employee.user.set_password(password)
		employee.user.save()

		template = loader.get_template('mus/emails/reset_password_%s.html' % employee.language_code)
		htmlbody = template.render(
				Context({
					'user': employee.user,
					'access_code': employee.getAccessCode(),
					'newpassword' : password
				})
			)
		send_mail(
			subject,
			strip_tags(htmlbody),
			settings.DEFAULT_FROM_MAIL,
			(employee.user.email,),
			html_message=htmlbody
		)
	def clean(self):
		super(PasswordResetForm, self).clean()
		if not 'email' in self.cleaned_data or not User.objects.filter(email__exact=self.cleaned_data['email']).exists():
			raise forms.ValidationError(_('Unknown email'))
		return self.cleaned_data
class EmployeeForm(forms.Form):
	"""
	Create employee form
	"""
	company = forms.ModelChoiceField(queryset=Company.objects.all(),required=True,widget=forms.HiddenInput())
	first_name = forms.CharField(label = _(u'First name'), max_length = 100,widget=forms.TextInput(attrs={'class':"form-control"}))
	last_name = forms.CharField(label = _(u'Last name'), max_length = 100,widget=forms.TextInput(attrs={'class':"form-control"}))
	user_name = forms.CharField(label = _(u'Username'), max_length = 75,widget=forms.TextInput(attrs={'class':"form-control"}))
	email = forms.EmailField(label=_(u'Email'),widget=forms.TextInput(attrs={'class':"form-control"}))
	confirm_email = forms.EmailField(label = _('Repeat email'),widget=forms.TextInput(attrs={'class':"form-control"}))
	development_plan_type = forms.ModelChoiceField(label=_('Type'),queryset=DevelopmentPlanType.objects.all(),empty_label=_('choose type'),widget=forms.Select(attrs={'class':"form-control"}))
	language_code = forms.ChoiceField(label=_("Language"),choices=settings.LANGUAGES,widget=forms.Select(attrs={'class':"form-control"}))
	manager = forms.ModelChoiceField(label=_('Manager'), queryset=Employee.objects.filter(is_manager=True), empty_label=_("choose manager"), required=False,widget=forms.Select(attrs={'class':"form-control"}))
	is_manager = forms.BooleanField(required = False, label = _('Create as manager'))

	def __init__(self, request, *args, **kwargs):
		self.request = request
		self.user = request.user
		super(EmployeeForm, self).__init__(*args, **kwargs)

	def save(self):
		"""
		Save form and send welcome mail (currently disabled)
		"""
		employee = Employee.objects.get(user__pk = self.user.pk)

		if not employee.isEnsoUser():
			if not employee.is_manager and not employee.isCompanySuperUserOrHigher():
				logUnauthorizedAccess("User tried to EmployeeForm. Accesscheck: 1", self.request)
				raise PermissionDenied()
			if self.cleaned_data.get('is_manager') and not employee.isCompanySuperUserOrHigher():
				logUnauthorizedAccess("User tried to EmployeeForm. Accesscheck: 2", self.request)
				raise PermissionDenied()
			if self.cleaned_data.get('company') != employee.company:
				logUnauthorizedAccess("User tried to EmployeeForm. Accesscheck: 3", self.request)
				raise PermissionDenied()

		password = generate_password(8)
		user = User.objects.create_user(
				username = self.cleaned_data.get('user_name'),
				email = self.cleaned_data.get('email'),
				password = password
				)
		user.first_name = self.cleaned_data.get('first_name')
		user.last_name = self.cleaned_data.get('last_name')
		user.save()
		manager = self.cleaned_data.get('manager')
		Employee.objects.create(
				user = user,
				manager = manager,
				is_manager = self.cleaned_data.get('is_manager'),
				company = self.cleaned_data.get('company'),
				created_by = self.user,
				updated_by = self.user,
				development_plan_type = self.cleaned_data.get('development_plan_type'),
				language_code = self.cleaned_data.get('language_code'),
				plaintext_password = my_encrypt(password)
		)
		#self._sendWelcomeMail(user, self.cleaned_data.get('password'))

	def _sendWelcomeMail(self, user, password):
		"""
		Send welcome mail to user
		"""
		template = loader.get_template('mus/create_user_mail.tpl')
		send_mail(
			settings.WELCOME_MAIL_SUBJECT,
			template.render(
				Context({
					'user': user,
					'password': password,
					'url': self.request.build_absolute_uri('/login/'),
					'sender': self.user
				})
			),
			self.user.email,
			[user.email]
		)


	def clean(self):
		"""
		Do validation
		"""
		super(EmployeeForm, self).clean()

		username = self.cleaned_data.get('user_name')

		if username:

			if not Employee.isValidUsername(username):
				raise forms.ValidationError(_(
					'Invalid username format. Accepted characters are A-Z,a-z,0-9,_-,.'
				))

			if User.objects.filter(username__exact = username).exists():
				raise forms.ValidationError(_('A user with the given username already exists'))

		email = self.cleaned_data.get('email')
		confirm_email = self.cleaned_data.get('confirm_email')
		if not email == confirm_email:
			raise forms.ValidationError(_('The emails are not equal'))
		if User.objects.filter(email__exact = self.cleaned_data.get('email')).exists():
			raise forms.ValidationError(_('A user with the given email already exists'))
		return self.cleaned_data

class EditEmployeeForm(forms.Form):
	"""
	Edit employee form
	"""
	first_name = forms.CharField(label = _(u'First name'), max_length = 100,widget=forms.TextInput(attrs={'class':"form-control"}))
	last_name = forms.CharField(label = _(u'Last name'), max_length = 100,widget=forms.TextInput(attrs={'class':"form-control"}))
	email = forms.EmailField(label=_(u'Email'),widget=forms.TextInput(attrs={'class':"form-control"}))
	language_code = forms.ChoiceField(label=_("Language"),choices=settings.LANGUAGES,widget=forms.Select(attrs={'class':"form-control"}))
	development_plan_type = forms.ModelChoiceField(label=_('Type'),queryset=DevelopmentPlanType.objects.all(),empty_label=_('choose type'),widget=forms.Select(attrs={'class':"form-control"}))
	old_password = forms.CharField(label = _('Password'), widget = forms.PasswordInput(attrs={'class':"form-control"}), required = False)
	password = forms.CharField(label = _('New password'), widget=forms.PasswordInput(attrs={'class':"form-control"}), required = False)
	confirm_password = forms.CharField(label = _('Repeat password'), widget=forms.PasswordInput(attrs={'class':"form-control"}),required=False)
	manager = forms.ModelChoiceField(label=_('Manager'), queryset=Employee.objects.filter(is_manager=True), empty_label=_("choose manager"), required=False,widget=forms.Select(attrs={'class':"form-control"}))
	is_manager = forms.BooleanField(required = False, label = 'Leder')

	def __init__(self, user, employee, *args, **kwargs):
		self.user = user
		self.employee = employee
		self.current_employee =Employee.objects.get(user__pk = self.user.pk)
		super(EditEmployeeForm, self).__init__(*args, **kwargs)
		self.fields['manager'].initial=self.employee.manager
		if not self.current_employee.isCompanySuperUserOrHigher():
			del self.fields['is_manager']
			del self.fields['manager']
			del self.fields['development_plan_type']

	def save(self):
		"""
		Save form
		"""
		if not self.current_employee.isCompanySuperUserOrHigher() and not self.user.pk == self.employee.user.pk and not self.user.pk == self.employee.manager.user.pk:
			raise PermissionDenied()
		self.employee.user.first_name = self.cleaned_data.get('first_name')
		self.employee.user.last_name = self.cleaned_data.get('last_name')
		self.employee.user.email = self.cleaned_data.get('email')
		if not self.cleaned_data.get('password') is None and len(self.cleaned_data.get('password')) > 5:
			self.employee.user.set_password(self.cleaned_data.get('password'))
			self.employee.plaintext_password = my_encrypt(self.cleaned_data.get('password'))
		if self.current_employee.isCompanySuperUserOrHigher():
			self.employee.development_plan_type = self.cleaned_data.get('development_plan_type')
			if not self.cleaned_data.get('manager') is None:
				manager = self.cleaned_data.get('manager')
				self.employee.manager = manager
			self.employee.is_manager = self.cleaned_data.get('is_manager')
		self.employee.language_code = self.cleaned_data.get('language_code')
		self.employee.user.save()
		self.employee.save()

	def clean(self):
		"""
		Validate
		"""
		password = self.cleaned_data.get('password', None)
		confirm_password = self.cleaned_data.get('confirm_password', None)
		if not password == confirm_password:
			raise forms.ValidationError(_(u'The passwords are not equal'))
		old_password = self.cleaned_data.get('old_password', None)
		if not len(password) == 0 and not self.user.check_password(old_password):
			raise forms.ValidationError(_('Wrong password given'))
		if not len(old_password) == 0 and not len(password) > 5:
			raise forms.ValidationError(_(u'The password need to have be at least 6 characters'))
		if User.objects.filter(email__exact = self.cleaned_data.get('email')).exclude(pk = self.employee.user.pk).exists():
			raise forms.ValidationError(_(u'A user with the given email already exists'))
		return self.cleaned_data
class AttachMUSForm(forms.Form):
	"""
	Form to attach development plan to employees
	"""
	email_text = forms.CharField(required=False,widget = forms.Textarea(attrs={'placeholder':_("Add a personal message (optional)")}))
	template = forms.ChoiceField(label=_("Template"),choices=settings.LANGUAGES,widget=forms.Select(attrs={'class':"form-control"}))
	employees = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple,queryset=Employee.objects.all())
	competence_fields = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple,queryset=CompetenceField.objects.filter(is_system=False,parent=None))

class ActionForm(forms.ModelForm):
	"""
	Model form for action
	"""

	description = forms.CharField(
		widget=forms.Textarea,
		max_length=500,
		label = _(u'My goal')
	)

	difficulty = forms.ChoiceField(label=_("Difficulty"),choices=Action.getDifficultyChoices(),widget=forms.Select(attrs={'class':"form-control"}))
	type = forms.ChoiceField(label=_("Type"),choices=Action.getTypeChoices(),widget=forms.Select(attrs={'class':"form-control"}))

	class Meta:
		model=Action
		fields =['title','description','my_effort','my_needs', 'difficulty', 'type']

	def save(self,current_user,employee,*args,**kwargs):
		"""
		Save form
		"""
		self.instance.sort_order = 1
		if not self.instance.pk:
			self.instance.created_by = current_user
			self.instance.employee = employee
		self.instance.updated_by = current_user
		action = super(ActionForm, self).save(*args,**kwargs)
		action.save()
		action.send_approval_notification()

DATE_INPUT_FORMATS = ['%Y-%m-%d',       # '2006-10-25'
'%m/%d/%Y',       # '10/25/2006'
'%d-%m-%Y',       # '10/25/2006'
'%m/%d/%y']       # '10/25/06'
class ActionCommentForm(forms.ModelForm):
	"""
	Form for action comment
	"""
	follow_up_at = forms.DateField(required=False,input_formats=DATE_INPUT_FORMATS,widget=forms.DateInput(attrs={'class':'form-control'}))
	reminder_at = forms.DateField(required=False,input_formats=DATE_INPUT_FORMATS,widget=forms.DateInput(attrs={'class':'form-control'}))

	class Meta:
		model=ActionComment
		fields = ['status','text','follow_up_at', 'reminder_at']
		widgets = {
			'text': forms.Textarea(attrs={'class':'form-control'}),
			'status': forms.Select(attrs={'class':'form-control'}),
			}

	def save(self,current_user,action,*args,**kwargs):
		"""
		Save form
		"""
		if not self.instance.pk:
			self.instance.created_by = current_user
		self.instance.updated_by = current_user
		self.instance.action = action
		action.follow_up_at = self.instance.follow_up_at
		if self.instance.status:
			action.status = self.instance.status
		action.save()
		action_comment = super(ActionCommentForm,self).save(*args,**kwargs)
		action_comment.save()

		if action.employee.user == current_user:
			self.instance.sendCommentNotification(1, action.employee.manager.user, current_user)
		else:
			self.instance.sendCommentNotification(2, action.employee.user, current_user)

		if self.cleaned_data['reminder_at']:

			at = time(0, 0, 0, 0, tzinfo=utc)
			follow_up_at = None

			if 'follow_up_at' in self.cleaned_data:
				follow_up_at = datetime.combine(self.cleaned_data['follow_up_at'], at)

			Reminder.create(
				ReminderTemplate.ID_CONTRIBUTION_KEY,
				send_date=datetime.combine(self.cleaned_data['reminder_at'], at),
				date=follow_up_at,
				comment=self.cleaned_data['text'],
				created_by=current_user
			)


class UploadEmployeesForm(forms.Form):
	"""
	Form for uploading csv file to create manye employee
	"""
	file = forms.FileField()
	def clean(self):

		if not 'file' in self.cleaned_data:
			raise forms.ValidationError("Missing file")

		filename = self.cleaned_data['file'].name
		ext = os.path.splitext(filename)[1]
		ext = ext.lower()
		if ext not in ['.csv']:
			raise forms.ValidationError("Not allowed filetype!")


def validate_uniqueemail(value):
	"""
	Make sure email doesn't already exist
	"""
	if User.objects.filter(email__exact = value).exists():
			raise forms.ValidationError(_(u'An user with the given email already exists'))

def validate_uniqueusername(value):
	"""
	Make sure username doesn't already exist
	"""
	if User.objects.filter(username__exact = value).exists():
			raise forms.ValidationError(_(u'An user with the given username already exists'))
class EmployeeRowForm(forms.Form):
	"""
	Form for each line in create many employees
	"""
	first_name = forms.CharField(label=_(u'First name'))
	last_name = forms.CharField(label=_(u'Last name'))
	username = forms.CharField(label=_(u'Username'),validators=[validate_uniqueusername])
	email = forms.EmailField(label=_(u'Email'),validators=[validate_uniqueemail])
	language_code = forms.ChoiceField(label=_("Language"),choices=settings.LANGUAGES,widget=forms.Select(attrs={'class':"form-control"}))
	development_plan_type = forms.ModelChoiceField(label=_('Type'),initial=1,queryset=DevelopmentPlanType.objects.all(),empty_label=_('choose type'),widget=forms.Select(attrs={'class':"form-control"}))
	is_manager = forms.BooleanField(label=_(u'Is manager'),initial=False,required=False)
	def save(self,current_user,company):
		"""
		Save form
		"""
		employee = current_user.employee_user.first()
		if not employee.is_manager and not employee.isCompanySuperUserOrHigher():
			raise PermissionDenied()
		if company != employee.company and not employee.isEnsoUser():
			raise PermissionDenied()
		password = generate_password(8)
		user = User.objects.create_user(
				username = self.cleaned_data.get('username').strip(),
				email = self.cleaned_data.get('email'),
				password = password
				)
		user.first_name = self.cleaned_data.get('first_name')
		user.last_name = self.cleaned_data.get('last_name')
		user.save()
		return Employee.objects.create(
				user = user,
				manager = None,
				is_manager = self.cleaned_data.get('is_manager'),
				company = company,
				created_by = current_user,
				updated_by = current_user,
				development_plan_type = self.cleaned_data.get('development_plan_type'),
				language_code = self.cleaned_data.get('language_code'),
				plaintext_password = my_encrypt(password)
		)

	def clean(self):
		if any(self.errors):
			return

		username = self.cleaned_data['username'].strip()

		if username:

			if not Employee.isValidUsername(username):
				raise forms.ValidationError(_(
					'Invalid username format. Accepted characters are A-Z,a-z,0-9,_-,.'
				))

			if User.objects.filter(username__exact = username).exists():
				raise forms.ValidationError(_('A user with the given username already exists'))

		return self.cleaned_data

class EmployeeManagerRowForm(forms.Form):
	"""
	Form for setting manager for each employee in create many employees
	"""
	employee = forms.ModelChoiceField(label=_('Employee'), queryset=Employee.objects.filter(), required=True,widget=widgets.PlainTextWidget(model=Employee))
	manager = forms.ModelChoiceField(label=_('Manager'), queryset=Employee.objects.filter(is_manager=True), empty_label=_("choose manager"), required=False,widget=forms.Select(attrs={'class':"form-control"}))
	def save(self,current_user):
		"""
		Save form
		"""
		employee = current_user.employee_user.first()
		if not employee.is_manager and not employee.isCompanySuperUserOrHigher():
			raise PermissionDenied()
		employee =  self.cleaned_data.get('employee')
		employee.manager = self.cleaned_data.get('manager')
		employee.save()
EmployeeManagerRowFormSet = formset_factory(EmployeeManagerRowForm,extra=0)      

class BaseEmployeeRowFormSet(BaseFormSet):
	def __init__(self, *args, **kwargs):
		super(BaseEmployeeRowFormSet, self).__init__(*args, **kwargs)
		for form in self.forms:
			form.empty_permitted = False
	def clean(self):
		if any(self.errors):
			return
		return self.cleaned_data

EmployeeRowFormSet = formset_factory(EmployeeRowForm,extra=0,formset=BaseEmployeeRowFormSet)

class ChangeCompanyForm(forms.Form):
	"""
	Form to change company
	"""
	company = forms.ModelChoiceField(label=_('company'),queryset=Company.objects.all(),required=True,widget=forms.Select(attrs={'class':"form-control"}))


class EmployeeNoteForm(forms.ModelForm):
	"""
	Model form for EmployeeNoteForm
	"""

	notes = forms.CharField(
		widget=forms.Textarea(attrs={'class' : 'col-md-10'}),
		label = _(u'Notes')
	)

	class Meta:
		model = Employee
		fields = ['notes']

	def save(self,current_user,employee,*args,**kwargs):
		"""
		Save form
		"""

		empl = super(EmployeeNoteForm, self).save(*args,**kwargs)
		empl.save()


class MultiLeaderModelForm(forms.Form):
	"""
	Form to create a leader model for multiple employees
	"""
	employees = forms.ModelMultipleChoiceField(
		widget=forms.SelectMultiple,queryset=Employee.objects.all()
	)

class UploadFileToEmployeyForm(forms.Form):
	"""
	Form for uploading files to an employee
	"""
	file = forms.FileField()

	def __init__(self, post=None, files=None):
		forms.Form.__init__(self, post, files)
		self.upload_status = 'OK' if 'upload_status' in get_current_request().GET else ''

	def clean_file(self):

		filename = self.cleaned_data.get('file').name
		ext = os.path.splitext(filename)[1]
		ext = ext.lower()
		if ext not in ['.png', '.jpg', '.doc', '.pdf']:
			raise forms.ValidationError("Not an allowed filetype!")

	def handle_upload(self, employee_id, f):

		user_dir = util.get_user_files_dir(employee_id)

		with open(os.path.join(user_dir, f.name), 'wb+') as dst:
			for chunk in f.chunks():
				dst.write(chunk)