import unittest
# from django.utils import unittest
from mock import Mock, patch
import ensomus.apps.mus.models as models
import django

django.setup()


# noinspection PyUnresolvedReferences
class EmployeeTest(unittest.TestCase):

	def test_isEnsoUserSuccess(self):

		currentEmpl = models.Employee()

		with patch.object(models.Employee, 'roles') as mock_roles:

			mock_roles.count.return_value = 1

			mock_filter = Mock()
			mock_filter.exists.return_value = True
			mock_roles.filter.return_value = mock_filter

			self.assertTrue(currentEmpl.isEnsoUser())
			mock_roles.filter.assert_called_with(name = u'Enso-bruger')

	def test_isEnsoUserFalseWrongRole(self):

		currentEmpl = models.Employee()

		with patch.object(models.Employee, 'roles') as mock_roles:

			mock_roles.count.return_value = 1

			mock_filter = Mock()
			mock_filter.exists.return_value = False
			mock_roles.filter.return_value = mock_filter

			self.assertFalse(currentEmpl.isEnsoUser())
			mock_roles.filter.assert_called_with(name = u'Enso-bruger')


	def test_isEnsoUserFalseZeroRoles(self):

		currentEmpl = models.Employee()

		with patch.object(models.Employee, 'roles') as mock_roles:
			mock_roles.count.return_value = 0
			self.assertFalse(currentEmpl.isEnsoUser())

	def test_isCompanySuperUserOrHigherFalseZeroRoles(self):

		currentEmpl = models.Employee()

		with patch.object(models.Employee, 'roles') as mock_roles:
			mock_roles.count.return_value = 0
			self.assertFalse(currentEmpl.isCompanySuperUserOrHigher())

	def test_isCompanySuperUserOrHigherSuccess(self):

		currentEmpl = models.Employee()

		with patch.object(models.Employee, 'roles') as mock_roles:
			mock_roles.count.return_value = 1
			self.assertTrue(currentEmpl.isCompanySuperUserOrHigher())


	def test_hasAccessSuccessToIsEnsoUser(self):

		currentEmpl = models.Employee()
		currentEmpl.isEnsoUser = Mock(return_value=True)
		self.assertTrue(currentEmpl.hasAccessTo(None))


	def test_hasAccessSuccessTargetIsCurrentUser(self):

		currentEmpl = models.Employee()
		currentEmpl.pk = 1
		currentEmpl.isEnsoUser = Mock(return_value=False)

		targetEmpl = models.Employee()
		targetEmpl.pk = 1

		self.assertTrue(currentEmpl.hasAccessTo(targetEmpl))


	def test_hasAccessSuccessIsManagerInSameCompany(self):

		comp = models.Company(pk=1)

		currentEmpl = models.Employee(pk=1, company=comp, is_manager=True)
		currentEmpl.isEnsoUser = Mock(return_value=False)

		targetEmpl = models.Employee(pk=2, company=comp)

		self.assertTrue(currentEmpl.hasAccessTo(targetEmpl))

	def test_hasAccessSuccessIsSuperUserOrHigher(self):

		comp = models.Company(pk=1)

		currentEmpl = models.Employee(pk=1, company=comp, is_manager=False)
		currentEmpl.isEnsoUser = Mock(return_value=False)
		currentEmpl.isCompanySuperUserOrHigher = Mock(return_value=True)

		tarcomp = models.Company(pk=2)
		targetEmpl = models.Employee(pk=2, company=tarcomp)

		self.assertTrue(currentEmpl.hasAccessTo(targetEmpl))


	def test_hasAccessFailureIsManagerButNotSameCompany(self):

		comp = models.Company(pk=1)

		currentEmpl = models.Employee(pk=1, company=comp, is_manager=True)
		currentEmpl.isEnsoUser = Mock(return_value=False)
		currentEmpl.isCompanySuperUserOrHigher = Mock(return_value=False)

		tarcomp = models.Company(pk=2)
		targetEmpl = models.Employee(pk=2, company=tarcomp)

		self.assertFalse(currentEmpl.hasAccessTo(targetEmpl))

	def test_isValidUsername(self):

		invalidUnicodeChars = [
			"\xc2", "\xc3", "\xa8", "\xa5",
			"\xe6", "\xf8", "\xe5", # danish ae, oe, aa
		]

		validASCIICodes = [45, 46] + range(48, 58) + range(65, 91) + [95] + range(97, 123)

		for char in invalidUnicodeChars:
			self.assertFalse(models.Employee.isValidUsername(char))

		for i in range(0, 256):
			if i in validASCIICodes:
				self.assertTrue(models.Employee.isValidUsername(
					chr(i)), "char: '{}' ASCII: '{}' was invalid.".format(chr(i), i)
				)
			else:
				self.assertFalse(models.Employee.isValidUsername(
					chr(i)), "char: '{}' ASCII: '{}' was valid".format(chr(i), i)
				)




