from django.contrib.auth.models import User

class EmployeeModel():
	pass

class RoleModel():

	def __init__(self, *args, **kwargs):
		self.name = kwargs['name']

	def getName(self):
		return self.name

class UserModel():

	def __init__(self, *args, **kwargs):
		if kwargs.has_key('pk'):
			self._loadUserByPrimaryKey(kwargs['pk'])
		elif kwargs.has_key('username'):
			self._loadUserByUserName(kwargs['username'])
		else:
			self.user = User()

	def _loadUserByPrimaryKey(self, pk):
		self.user = User.objects.get(pk = pk)

	def _loadUserByUserName(self, username):
		self.user = User.objects.get(username = username)

	def save(self):
		User.save(self)