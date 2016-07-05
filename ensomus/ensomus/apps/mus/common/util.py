from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.conf import settings
import cStringIO as StringIO
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
import csv
import HTMLParser
import json
import hashlib
import string
import random
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
import logging
import os

logger = logging.getLogger(__name__)

def safeHtmlString(string, length):
	html_parser = HTMLParser.HTMLParser()
	un_escaped_string = html_parser.unescape(mark_safe(strip_tags(string)))
	if (len(string) > length):
		return un_escaped_string[:length] + ' . . .'
	return un_escaped_string

def replaceAllText(text, is_employee):
	for mapping in settings.TEXT_MAPPING:
		replace_with = settings.TEXT_MAPPING[mapping]['Employee']
		if  not is_employee:
			replace_with = settings.TEXT_MAPPING[mapping]['Manager']
		text = text.replace(mapping, replace_with)
	return text
def render_to_pdf(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	result = StringIO.StringIO()

	pdf = pisa.pisaDocument(StringIO.StringIO(html), dest=result, encoding="UTF-8")
	if not pdf.err:
		return HttpResponse(result.getvalue(), mimetype='application/pdf')
	return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def write_pdf(template_src, context_dict, filename):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	html = html.replace('<li>','<li><img class="square" src="http://test.nxtlvl.dk/static/img/square.png" />')
	result = open(filename, 'wb') # Changed from file to filename
	pdf = pisa.pisaDocument(StringIO.StringIO(
		html.encode("UTF-8")), dest=result)
	result.close()

def fetch_resources(uri, rel):
	path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.STATIC_URL, ""))

	return path

def utf_8_encoder(unicode_csv_data):
	for line in unicode_csv_data:
		yield line.decode('iso-8859-1').encode('UTF-8')
def csv_to_dict(file):
	data = list()
	reader = csv.reader(utf_8_encoder(file))
	for row in reader:
		data.append(row)
	return data

class LazyEncoder(DjangoJSONEncoder):
	def default(self, obj):
		if isinstance(obj, Promise):
			return force_text(obj)
		return super(LazyEncoder, self).default(obj)

def my_encrypt(s1):    
	s2 = hashlib.md5("--1h3olllvq*3(esrmaisz0w1(jdx^ov4@*q&amp;v2m+3^^tzyn$*").digest()
	return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2)).encode('hex')
def my_decrypt(s1):    
	s2 = hashlib.md5("--1h3olllvq*3(esrmaisz0w1(jdx^ov4@*q&amp;v2m+3^^tzyn$*").digest()
	return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1.decode('hex'),s2))

def generate_password(length):
	chars = string.letters + string.digits
	return ''.join(map(lambda x: random.choice(chars), range(length)))

def getRequestDetails(request):
	"""

	:param request:
	:return: string
	"""
	details = "Request: {}".format(request)
	return details

def logUnauthorizedAccess(msg, request, data=None):
	"""

	:param msg: string
	:param request: WSGIRequest
	:param data: dict
	:return: None
	"""
	data = "Data:\n{}\n\n".format(data)

	logger.warning("Message: " + msg + "\n\n" + data + getRequestDetails(request))

def get_user_files_dir(employee_id):

	top_dir = os.path.join(settings.FILES_ROOT, 'employee_files')
	user_dir = os.path.join(top_dir, employee_id)

	if not os.path.isdir(top_dir):
		os.makedirs(top_dir)

	if not os.path.isdir(user_dir):
		os.makedirs(user_dir)

	return user_dir
