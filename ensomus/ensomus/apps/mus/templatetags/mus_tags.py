"""
Custom tags, functions and filters for NXT LVL
"""
from django import template
from ensomus.apps.mus.models import Employee
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import logging
import re 

register = template.Library()
logger = logging.getLogger(__name__)

@register.filter(name='currentEmployee')
def currentEmployee(user_pk):
	"""
	Filter: Get employee of user
	"""
	emp = None

	try:
		emp = Employee.objects.get(user__pk = user_pk)
	except ObjectDoesNotExist, e:
		logger.exception('Could not lookup Employee object on user_pk = "{}"'.format(user_pk))
		raise e

	return emp


@register.filter(name='currentEmployeeId')
def currentEmployeeId(user):
	"""
	Filter: Get employee id of user
	"""
	return currentEmployee(user.pk).id

@register.filter(name='isCompanySuperUserOrHigher')
def isCompanySuperUserOrHigher(user):
	"""
	Filter: is user super user or enso user
	"""
	return currentEmployee(user.pk).isCompanySuperUserOrHigher()

@register.filter(name='isManager')
def isManager(user):
	"""
	Filter: is user manager
	"""
	return currentEmployee(user.pk).is_manager

@register.filter(name='key')
def key(obj,k):
	"""
	Filter: get element of dictionary with key k
	"""
	try:
		return obj[k]
	except KeyError:
		return ''

@register.filter(name='key_exists')
def key_exists(obj,k):
	"""
	Filter: test if key exists in obj
	"""
	return k < len(obj)


@register.filter(name='range')
def get_range(obj):
	"""
	Filter: make range of number
	"""
	return range(obj)

@register.filter
def attr(obj, arg1):
	"""
	Filter: attach attribute to field widget
	"""
	att, value = arg1.split("=")
	if att == "class" and att in obj.field.widget.attrs:
		obj.field.widget.attrs[att] = "%s %s" % (value,obj.field.widget.attrs[att])
	else:
		obj.field.widget.attrs[att] = value
	return obj

@register.filter
def replace ( string, args ): 
	search  = args.split(args[0])[1]
	replace = args.split(args[0])[2]

	return re.sub( search, replace, string )

@register.assignment_tag
def in_debug_mode():
	"""
	Tag: is the site in debug mode
	"""
	return settings.DEBUG