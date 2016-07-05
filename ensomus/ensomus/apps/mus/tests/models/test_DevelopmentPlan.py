import unittest
from mock import Mock, patch, MagicMock
import ensomus.apps.mus.models as models
from django.contrib.auth.models import User
import django


django.setup()

# class mEmployee:
# 	pass

# noinspection PyUnresolvedReferences
class DevelopmentPlanTest(unittest.TestCase):

	def test_canManageIsEnsoUser(self):

		emps = models.Employee.objects.all()
		print(emps)

		return


		currentCompany = models.Company()
		currentCompany.pk = 1
		currentEmpl = models.Employee()
		currentEmpl.isEnsoUser = Mock(return_value=False)
		currentEmpl.company = currentCompany


		targetCompany = models.Company()
		targetCompany.pk = 2

		targetEmpl = models.Employee()
		muser = Mock(spec=User)
		muser._state = Mock()
		muser.id = 1
		try:
			targetEmpl.user = muser
		except ValueError:
			pass

		targetEmpl.company = targetCompany

		devplan = models.DevelopmentPlan()
		devplan.owner = targetEmpl

		self.assertTrue(devplan.canManage(currentEmpl))

		currentEmpl.isEnsoUser.assert_called_once_with()
		currentEmpl.isManager.assert_called_once_with()


		# currentCompany = models.Company()
		# currentCompany.pk = 1
		# currentEmpl = models.Employee()
		# currentEmpl.isEnsoUser = Mock(return_value=False)
		# currentEmpl.company = currentCompany
		#
		# targetCompany = models.Company()
		# targetCompany.pk = 2
		#
		# targetEmpl = models.Employee()
		# muser = Mock(spec=User)
		# muser._state = Mock()
		# muser.id = 1
		# try:
		# 	targetEmpl.user = muser
		# except ValueError:
		# 	pass
		#
		# targetEmpl.company = targetCompany
		#
		# devplan = models.DevelopmentPlan()
		# devplan.owner = targetEmpl
		#
		# self.assertTrue(devplan.canManage(currentEmpl))
		#
		# currentEmpl.isEnsoUser.assert_called_once_with()
		# currentEmpl.isManager.assert_called_once_with()


