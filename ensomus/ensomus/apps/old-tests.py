# coding=utf-8
import unittest
##import mock
from models import Company
##from models import CompetenceFieldCollectionToCompanyRelation
from models import Employee
#from models import CompetenceFieldCollectionToUserRelation, QuestionResponse, Question
from mus.models import DevelopmentPlan
from mus.models import CompetenceFieldCollectionToUserRelation
from mus.models import CompetenceFieldCollection
from mus.models import Assignment
from mus.models import AssignmentKey
from mus.models import AssignmentKeyToUserRelation
#from models import Employee, CompetenceField
#from mocks import EmployeeMock, CompetenceFieldCollectionToUserRelationMock
from mus.models import AssignmentResponse
from mus.models import ActionKeyToDevelopmentPlanRelation
from mus.models import ActionKey
from mus.common.util import replaceAllText
#from mocks import MethodCalledOnceMock, CreateGetMock, MethodCalledNoTimesMock, CompetenceFieldCollectionMock
#from mocks import CompetenceFieldMock, CompetenceMock, AllMock, CreateQuestionResponseMock
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Model
# from django.db.models.query import QuerySet
import datetime
#from django.db.models import ManyToManyField


class CompanyTest(unittest.TestCase):

	def test_getAvailableSchemesWithoutAConnectionHasBeenMadeExpectEmptyListIsReturned(self):
		company = Company()
		schemes = company.getAvailableSchemes()
		self.assertEqual(0, len(schemes))

	def test_callingGetAvailableSchemesCallsFilterOnCompetenceFieldCollectionToCompanyRelationWithCompanyPkAsArgument(self):
		company = Company()
		company.pk = 8
		with mock.patch.object(CompetenceFieldCollectionToCompanyRelation, 'objects') as query_mock:
			company.getAvailableSchemes()
			query_mock.filter.assert_called_with(company__pk=company.pk)


class EmployeeTest(unittest.TestCase):

	def test_callingGetEmployeesCallsFilterOnEmployeeWithCompanyPkAsArgumentAndIsMangerEqualToTrue(self):
		employee = Employee()
		company = Company()
		company.pk = 8
		employee.company = company
		with mock.patch.object(Employee, 'objects') as query_mock:
			employee.getEmployees()
			query_mock.filter.assert_called_with(company__pk=company.pk, is_manager=True)

	def test_callingGetMyEmployeesCallsFilterOnEmployeeWithCurrentUserPkAsArgumentToManager(self):
		employee = Employee()
		employee.pk = 2
		with mock.patch.object(Employee, 'objects') as query_mock:
			employee.getMyEmployees()
			query_mock.filter.assert_called_with(manager__pk=employee.pk)

	def test_callingGetMyEmployeesReturnsListOfEmployees(self):
		employee = Employee()
		employee.pk = 2
		with mock.patch.object(Employee, 'objects') as employee_mock:
			return_employee = Employee()
			return_employee.pk = 4
			return_employee.user = User()
			return_employee.user.first_name = 'Joachim'
			return_employee.user.last_name = 'Andersen'
			return_employee.manager = employee
			query_set_mock = mock.MagicMock()
			query_set_mock.order_by.return_value = iter([return_employee, ])
			employee_mock.filter.return_value = query_set_mock
			result = employee.getMyEmployees()
			self.assertTrue(isinstance(result[0], Employee))
			self.assertEqual(1, len(result))
			self.assertEqual(4, result[0].pk)
			self.assertEqual('Joachim', result[0].user.first_name)
			self.assertEqual('Andersen', result[0].user.last_name)

	def test_callingGetMyEmployeesCallsOrderByOnFilterResultWithLastNameThenFirstNameAsArguments(self):
		employee = Employee()
		employee.pk = 2
		with mock.patch.object(Employee, 'objects') as query_mock:
			return_employee = Employee()
			return_employee.pk = 4
			return_employee.user = User()
			return_employee.user.first_name = 'Joachim'
			return_employee.user.last_name = 'Andersen'
			return_employee.manager = employee
			employee.getMyEmployees()
			query_mock.filter.return_value.order_by.assert_called_with('user__last_name', 'user__first_name')

	def test_callingGetMyEmployeesWithEmployeeAsArgumentCallsFilterWithEmployeesPkAsArgument(self):
		master_employee = Employee()
		master_employee.pk = 2
		a_manager = Employee()
		a_manager.pk = 87
		with mock.patch.object(Employee, 'objects') as employee_mock:
			master_employee.getMyEmployees(a_manager)
			employee_mock.filter.assert_called_with(manager__pk=a_manager.pk)

	def test_callingGetEmployeesCallsGetMyEmployeesWithEmployeeAsArgument(self):
		Employee.objects.filter = mock.MagicMock()
		employee = Employee()
		employee.pk = 29
		employee.company = Company()
		employee.company.pk = 87
		employee.user = User()
		employee.user.first_name = 'Fornavn'
		employee.user.last_name = 'Efternavn'
		Employee.objects.filter.return_value = [employee, ]
		employee.getMyEmployees = mock.MagicMock()
		employee.getEmployees()
		employee.getMyEmployees.assert_called_once_with(manager=employee)

	def test_callingGetEmployeesCallsGetMyEmployeesOneTimePerManagerInSameCompanyAsCaller(self):
		Employee.objects.filter = mock.MagicMock()
		company = Company()
		company.pk = 98
		employee_one = Employee()
		employee_one.pk = 12
		employee_one.company = company
		employee_one.user = User()
		employee_one.user.first_name = 'Fornavn'
		employee_one.user.last_name = 'Efternavn'
		employee_two = Employee()
		employee_two.pk = 12
		employee_two.company = company
		employee_two.user = User()
		employee_two.user.first_name = 'Fornavn'
		employee_two.user.last_name = 'Efternavn'
		Employee.objects.filter.return_value = [employee_one, employee_two]
		employee_one.getMyEmployees = mock.MagicMock()
		employee_one.getEmployees()
		self.assertEquals(2, employee_one.getMyEmployees.call_count)

	def test_callingGetEmployeesReturnsListOfDicts(self):
		Employee.objects.filter = mock.MagicMock()
		company = Company()
		company.pk = 98
		employee_one = Employee()
		employee_one.pk = 12
		employee_one.user = User()
		employee_one.user.first_name = 'Fornavn'
		employee_one.user.last_name = 'Efternavn'
		employee_one.company = company
		employee_two = Employee()
		employee_two.pk = 13
		employee_two.user = User()
		employee_two.user.first_name = 'Fornavn'
		employee_two.user.last_name = 'Efternavn'
		employee_two.company = company
		Employee.objects.filter.return_value = [employee_one, employee_two]
		employee_one.getMyEmployees = mock.MagicMock()
		employee_one.getMyEmployees.return_value = []
		employee_list = employee_one.getEmployees()
		self.assertEquals(2, len(employee_list))
		self.assertTrue(isinstance(employee_list[0], dict))
		self.assertTrue(isinstance(employee_list[0]['manager'], Employee))
		self.assertEquals(employee_list[0]['manager'].pk, 12)
		self.assertTrue(isinstance(employee_list[0]['employees'], list))
		self.assertEquals(employee_list[0]['manager'].user.first_name, 'Fornavn')
		self.assertEquals(employee_list[0]['manager'].user.last_name, 'Efternavn')

	def test_callingGetDevelopmentPlansCallsFilterAndOrderByOnDevelopmentPlanWithGivenUserAsArgument(self):
		employee = Employee()
		employee.pk = 38
		employee.user = User()
		employee.user.pk = 9
		DevelopmentPlan.objects.filter = mock.MagicMock()
		DevelopmentPlan.objects.filter.return_value.order_by = mock.MagicMock()
		employee.getDevelopmentPlans()
		DevelopmentPlan.objects.filter.assert_called_once_with(owner__pk=38)
		DevelopmentPlan.objects.filter.return_value.order_by.assert_called_once_with('-created_at')

	def test_callingGetDevelopmentPlansReturnsListOfDevelopmentPlans(self):
		employee = Employee()
		employee.pk = 38
		employee.user = User()
		employee.user.pk = 9
		development_plan_one = DevelopmentPlan()
		development_plan_two = DevelopmentPlan()
		DevelopmentPlan.objects.filter = mock.MagicMock()
		DevelopmentPlan.objects.filter.return_value.order_by = mock.MagicMock()
		DevelopmentPlan.objects.filter.return_value.order_by.return_value = [development_plan_one, development_plan_two]
		development_plans = employee.getDevelopmentPlans()
		self.assertEquals(2, len(development_plans))
		self.assertTrue(isinstance(development_plans[0], DevelopmentPlan))

	def test_callingGetDevelopmentPlansWithAsManagerEqualToTrueCallsFilterWithOwnerManagerAsArgument(self):
		employee = Employee()
		employee.pk = 38
		DevelopmentPlan.objects.filter = mock.MagicMock()
		DevelopmentPlan.objects.filter.return_value.order_by = mock.MagicMock()
		employee.getDevelopmentPlans(as_manager=True)
		DevelopmentPlan.objects.filter.assert_called_once_with(owner__manager__pk=38)

	def test_callingCanAssociateNewPlanReturnsTrueIfTheEmployeeHasNoOpenDevelopmentPlans(self):
		employee = Employee()
		employee.pk = 38
		employee.user = User()
		employee.user.pk = 9
		CompetenceFieldCollectionToUserRelation.objects.filter = mock.MagicMock()
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.exists = mock.MagicMock()
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.exists.return_value = []
		self.assertTrue(employee.canAssociateNewPlan())
		CompetenceFieldCollectionToUserRelation.objects.filter.assert_called_once_with(user__pk=employee.user.pk, finished_at=None)

	def test_callingCanAssociateNewPlanReturnsFalseIfTheEmployeeHasAnOpenDevelopmentPlan(self):
		employee = Employee()
		employee.pk = 38
		employee.user = User()
		employee.user.pk = 9
		CompetenceFieldCollectionToUserRelation.objects.filter = mock.MagicMock()
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.exists = mock.MagicMock()
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.exists.return_value = [CompetenceFieldCollectionToUserRelation(employee.user, finished_at=None),]
		self.assertFalse(employee.canAssociateNewPlan())
		CompetenceFieldCollectionToUserRelation.objects.filter.assert_called_once_with(user__pk=employee.user.pk, finished_at=None)


class EmployeeDevelopmentPlanStatusTest(unittest.TestCase):

	def test_callingDevelopmentPlanStatusReturnsStringIfLastPlanIsOpen(self):
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.order_by.return_value = [CompetenceFieldCollectionToUserRelation(user=self.employee.user, finished_at=None),]
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.count.return_value = 1
		self.assertEquals(u'Åben', self.employee.developmentPlanStatus())
		CompetenceFieldCollectionToUserRelation.objects.filter.assert_called_with(user__pk=self.employee.user.pk)
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.order_by.assert_called_with('-finished_at')

	def test_callingDevelopmentPlanStatusReturnsStringIfLastPlanIsClosed(self):
		dt = datetime.datetime.now()
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.order_by.return_value = [CompetenceFieldCollectionToUserRelation(user=self.employee.user, finished_at=dt),]
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.count.return_value = 1
		self.assertEquals(dt.strftime(u'Lukket den %d. %B %Y'), self.employee.developmentPlanStatus())
		CompetenceFieldCollectionToUserRelation.objects.filter.assert_called_with(user__pk=self.employee.user.pk)
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.order_by.assert_called_with('-finished_at')

	def test_callingDevelopmentPlanStatusReturnsStringIfNoClosedPlansExists(self):
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.count.return_value = 1
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.order_by.return_value = [CompetenceFieldCollectionToUserRelation(user=self.employee.user, finished_at=None),]
		self.assertEquals(u'Åben', self.employee.developmentPlanStatus())
		CompetenceFieldCollectionToUserRelation.objects.filter.assert_called_with(user__pk=self.employee.user.pk)
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.order_by.assert_called_with('-finished_at')

	def test_callingDevelopmentPlanStatusReturnsStringIfNoPlanExists(self):
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.count.return_value = 0
		self.assertEquals(u'Ingen tilknytninger', self.employee.developmentPlanStatus())
		CompetenceFieldCollectionToUserRelation.objects.filter.assert_called_with(user__pk=self.employee.user.pk)

	def setUp(self):
		self.employee = Employee(pk=2, user=User(pk=9))
		CompetenceFieldCollectionToUserRelation.objects.filter = mock.MagicMock()
		CompetenceFieldCollectionToUserRelation.objects.filter.return_value.order_by = mock.MagicMock()


# class EmployeeDevelopmentPlansTest(unittest.TestCase):

#     def test_callingGetDevelopmentPlansForEmployee(self):
#         DevelopmentPlan.objects.filter.return_value.order_by.return_value = [DevelopmentPlan(owner=self.employee, created_at=datetime.datetime.now()),]
#         self.manager.getDevelopmentPlansForEmployee(self.employee.pk)
#         DevelopmentPlan.objects.filter.assert_called_once_with(owner__pk=self.employee.pk)
#         DevelopmentPlan.objects.filter.order_by.assert_called_once_with('-created_at')

#     def setUp(self):
#         DevelopmentPlan.objects.filter = mock.MagicMock()
#         DevelopmentPlan.objects.filter.return_value.order_by = mock.MagicMock()
#         self.manager = Employee(pk=2, user=User(pk=9), is_manager=True)
#         self.employee = Employee(pk=3, user=User(pk=10), is_manager=False, manager=self.manager)


class AssociateNewPlanTest(unittest.TestCase):

	def test_callingCreateDevelopmentPlanCallsCanAssociateNewPlan(self):
		self.employee.createDevelopmentPlan(1, self.employee.user)
		self.assertEquals(1, self.employee.canAssociateNewPlan.call_count)

	def test_calingCreateDevelopmentPlanReturnsNoneIfCanAssociateNewPlanReturnsFalse(self):
		development_plan = self.employee.createDevelopmentPlan(1, self.employee.user)
		self.assertEquals(None, development_plan)

	def setUp(self):
		self.employee = Employee(pk=2, user=User(pk=9))
		self.employee.canAssociateNewPlan = mock.MagicMock()
		self.employee.canAssociateNewPlan.return_value = False

	def tearDown(self):
		self.employee = None


class DevelopmentPlanMembersTest(unittest.TestCase):
	pass

class DevelopmentPlanTest(unittest.TestCase):

	def test_callingCreatePlanInstantiatesTwoCompetenceFieldCollectionToUserRelations(self):
		development_plan = self.employee.createDevelopmentPlan(1, self.current_user)
		self.assertTrue(isinstance(development_plan.employee_response_relation, CompetenceFieldCollectionToUserRelation))
		self.assertTrue(isinstance(development_plan.manager_response_relation, CompetenceFieldCollectionToUserRelation))
		self.assertEquals(2, CompetenceFieldCollectionToUserRelation.objects.create.call_count)
		CompetenceFieldCollectionToUserRelation.objects.create.assert_any_call(
			user=self.employee.user,
			competence_field_collection = CompetenceFieldCollection.objects.get(pk=1),
			created_by=self.current_user
			)
		CompetenceFieldCollectionToUserRelation.objects.create.assert_any_call(
			user=self.employee.manager.user,
			competence_field_collection = CompetenceFieldCollection.objects.get(pk=1),
			created_by=self.current_user
			)

	def test_callingCreatePlanSetsCreatedByToCurrentUserArgument(self):
		development_plan = self.employee.createDevelopmentPlan(1, self.current_user)
		self.assertEquals(self.current_user, development_plan.created_by)

	def test_callingCreatePlanCallsSaveOnBothCompetenceFieldCollectionToUserRelation(self):
		self.employee.createDevelopmentPlan(1, self.current_user)
		self.assertEquals(2, CompetenceFieldCollectionToUserRelation.save.call_count)

	def test_callingCreatePlanCallsSaveInsideATransaction(self):
		self.employee.createDevelopmentPlan(1, self.current_user)
		self.assertEquals(1, transaction.commit_on_success.call_count)

	def test_callingCreatePlanCallsSaveOnThePlan(self):
		development_plan = self.employee.createDevelopmentPlan(1, self.current_user)
		self.assertEquals(1, development_plan.save.call_count)

	def test_callingCreatePlansCallsCreatePlanOneTimePerEmployeePk(self):
		Employee.objects.get = mock.MagicMock()
		Employee.createDevelopmentPlan = mock.MagicMock()
		Employee.objects.get.return_value = Employee()
		Employee.objects.get.return_value.user = User()
		Employee.objects.get.return_value.manager = Employee()
		Employee.objects.get.return_value.manager.user = User()
		DevelopmentPlan.save = mock.MagicMock()
		self.employee.createDevelopmentPlans([1,3,4], 1, self.current_user)
		self.assertEquals(3, Employee.createDevelopmentPlan.call_count)

	def test_callingCreateDevelopmentPlanCreatesTwoAssignmentKeys(self):
		development_plan = self.employee.createDevelopmentPlan(1, self.current_user)
		self.assertTrue(isinstance(development_plan.employee_assignment_key_relation, AssignmentKeyToUserRelation))
		self.assertTrue(isinstance(development_plan.manager_assignment_key_relation, AssignmentKeyToUserRelation))
		self.assertEquals(2, AssignmentKeyToUserRelation.objects.create.call_count)
		AssignmentKeyToUserRelation.objects.create.assert_any_call(
			user=self.employee.user,
			assignment_key = AssignmentKey.objects.all()[0],
			created_by=self.current_user
			)
		AssignmentKeyToUserRelation.objects.create.assert_any_call(
			user=self.employee.manager.user,
			assignment_key = AssignmentKey.objects.all()[0],
			created_by=self.current_user
			)

	def setUp(self):
		transaction.commit_on_success = mock.MagicMock()
		CompetenceFieldCollectionToUserRelation.save = mock.MagicMock()
		CompetenceFieldCollectionToUserRelation.objects.create = mock.MagicMock()
		CompetenceFieldCollectionToUserRelation.objects.create.return_value = CompetenceFieldCollectionToUserRelation()
		CompetenceFieldCollection.objects.get = mock.MagicMock()
		AssignmentKeyToUserRelation.objects.create = mock.MagicMock()
		AssignmentKeyToUserRelation.objects.create.return_value = AssignmentKeyToUserRelation()
		AssignmentKey.objects.all = mock.MagicMock()
		AssignmentKey.objects.all.return_value = [AssignmentKey(),]
		DevelopmentPlan.save = mock.MagicMock()
		self.employee = Employee()
		self.employee.pk = 7
		self.employee.user = User()
		self.employee.user.pk = 32
		self.employee.manager = Employee()
		self.employee.manager.pk = 76
		self.employee.manager.user = User()
		self.employee.manager.user.pk = 99
		self.current_user = self.employee.manager.user


class ActionKeyToDevelopmentPlanRelationLockUnlockTest(unittest.TestCase):

	def test_callingLockSetsIsLockedToTrue(self):
		self.assertFalse(self.action_key_to_development_plan_relation.is_locked)
		self.action_key_to_development_plan_relation.lock()
		self.assertTrue(self.action_key_to_development_plan_relation.is_locked)
		self.assertEquals(1, ActionKeyToDevelopmentPlanRelation.save.call_count)

	def test_callingUnLockSetsIsLockedToFalseIfEmployeeIsSuperUser(self):
		self.action_key_to_development_plan_relation.lock()
		self.assertTrue(self.action_key_to_development_plan_relation.is_locked)
		Employee.isCompanySuperUserOrHigher = mock.MagicMock()
		Employee.isCompanySuperUserOrHigher.return_value = True
		self.action_key_to_development_plan_relation.unLock(Employee())
		self.assertFalse(self.action_key_to_development_plan_relation.is_locked)
		self.assertEquals(2, ActionKeyToDevelopmentPlanRelation.save.call_count)

	def test_callingUnLockDoesNothingIfEmployeeIsNotSuperUser(self):
		self.action_key_to_development_plan_relation.lock()
		self.assertTrue(self.action_key_to_development_plan_relation.is_locked)
		Employee.isCompanySuperUserOrHigher = mock.MagicMock()
		Employee.isCompanySuperUserOrHigher.return_value = False
		self.action_key_to_development_plan_relation.unLock(Employee())
		self.assertTrue(self.action_key_to_development_plan_relation.is_locked)
		self.assertEquals(1, ActionKeyToDevelopmentPlanRelation.save.call_count)

	def setUp(self):
		ActionKeyToDevelopmentPlanRelation.save = mock.MagicMock()
		self.action_key_to_development_plan_relation = ActionKeyToDevelopmentPlanRelation()


class ActionKeyToDevelopmentPlanRelationTest(unittest.TestCase):

	def test_callingConnectActionKeyCallsCreateOnActionKeyToDevelopmentPlanRelation(self):
		self.development_plan.connectActionKey(self.user)
		ActionKeyToDevelopmentPlanRelation.objects.create.assert_called_once_with(
			action_key=self.action_keys[0],
			development_plan_relation=self.development_plan,
			created_by=self.user
			)

	def test_callingConnectActionKeyCallsSaveOnTheCreatedActionKeyToDevelopmentPlanRelation(self):
		action_key_to_development_plan_relation = self.development_plan.connectActionKey(self.user)
		self.assertEquals(1, action_key_to_development_plan_relation.save.call_count)

	def test_callingGetActionKeysCallsFilterOnActionKeyToDevelopmentPlanRelationWithTheExpectedArguments(self):
		self.development_plan.getActionKeys()
		ActionKeyToDevelopmentPlanRelation.objects.filter.assert_called_once_with(
			development_plan_relation=self.development_plan
			)

	def test_callingGetActionKeysCallsOrderByOnActionKeyToDevelopmentPlanRelationWithTheExpectedArguments(self):
		self.development_plan.getActionKeys()
		ActionKeyToDevelopmentPlanRelation.objects.filter.return_value.order_by.assert_called_once_with('-created_at')

	def test_callingGetActionKeysReturnsListOfDicts(self):
		action_key_to_development_plan_relations = self.development_plan.getActionKeys()
		self.assertTrue(isinstance(action_key_to_development_plan_relations[0], dict))
		self.assertEquals(4, action_key_to_development_plan_relations[0].get('pk'))
		self.assertEquals('title', action_key_to_development_plan_relations[0].get('title'))
		self.assertEquals(1, action_key_to_development_plan_relations[0].get('action_key_pk'))

	def setUp(self):
		ActionKeyToDevelopmentPlanRelation.action_key = mock.MagicMock()
		ActionKeyToDevelopmentPlanRelation.action_key.title = 'title'
		ActionKeyToDevelopmentPlanRelation.action_key.pk = 1
		ActionKeyToDevelopmentPlanRelation.objects.create = mock.MagicMock()
		ActionKeyToDevelopmentPlanRelation.save = mock.MagicMock()
		ActionKeyToDevelopmentPlanRelation.objects.filter = mock.MagicMock()
		ActionKeyToDevelopmentPlanRelation.objects.filter.return_value.order_by = mock.MagicMock()
		ActionKeyToDevelopmentPlanRelation.objects.filter.return_value.order_by.return_value = [
			ActionKeyToDevelopmentPlanRelation(pk=4),
			ActionKeyToDevelopmentPlanRelation(pk=2)
		]
		ActionKey.objects.all = mock.MagicMock()
		self.action_keys = [ActionKey(pk=1), ]
		ActionKey.objects.all.return_value = self.action_keys
		self.development_plan = DevelopmentPlan()
		self.user = User(pk=3)


class AssignmentKeyToUserRelationTest(unittest.TestCase):

	def test_callingGetAssignmentKeyReturnsTheAssignmentKey(self):
		assignment_key_to_user_relation = self.development_plan.getAssignmentKey(1)
		AssignmentKeyToUserRelation.objects.get.assert_called_once_with(pk=1)
		self.assertTrue(isinstance(assignment_key_to_user_relation, AssignmentKeyToUserRelation))

	def setUp(self):
		AssignmentKeyToUserRelation.objects.get = mock.MagicMock()
		AssignmentKeyToUserRelation.objects.get.return_value = AssignmentKeyToUserRelation()
		self.development_plan = DevelopmentPlan()


class AssignmentKeyToUserRelationGetResponsesTest(unittest.TestCase):

	def test_callingGetResponsesReturnsListOfAssignmentResponses(self):
		AssignmentResponse.objects.filter.return_value.order_by.return_value = [AssignmentResponse(pk=1), ]
		assignment_responses = self.assignment_key_to_user_relation.getResponses()
		self.assertTrue(isinstance(assignment_responses[0], AssignmentResponse))
		AssignmentResponse.objects.filter.assert_called_once_with(assignment_key_to_user_relation__pk=84)
		AssignmentResponse.objects.filter.return_value.order_by.assert_called_once_with('assignment__sort_order')

	def test_callingGetResponsesCreatesOneEmptyResponsePerAssignmentIfTheyAreNotAllreadyThere(self):
		AssignmentResponse.objects.filter.return_value.order_by.return_value = []
		self.assignment_key_to_user_relation.getResponses()
		self.assertEquals(1, Assignment.objects.all.call_count)
		self.assertEquals(2, AssignmentResponse.objects.create.call_count)
		AssignmentResponse.objects.create.assert_any_call(
			assignment=self.assignments[0],
			assignment_key_to_user_relation=self.assignment_key_to_user_relation
			)
		AssignmentResponse.objects.create.assert_any_call(
			assignment=self.assignments[1],
			assignment_key_to_user_relation=self.assignment_key_to_user_relation
			)

	def test_callingGetClientResponsesCallsGetResponsesAndReturnsDataAsListOfDicts(self):
		self.assignment_key_to_user_relation.getResponses = mock.MagicMock()
		self.assignment_key_to_user_relation.getResponses.return_value = [
			AssignmentResponse(
				pk=10,
				assignment=Assignment(pk=8,title='Assignment title'),
				text_assignment='Assignment text',
				text_competence='Competence text'
				)
		]
		assignment_responses = self.assignment_key_to_user_relation.getClientResponses()
		self.assertEquals(1, self.assignment_key_to_user_relation.getResponses.call_count)
		self.assertTrue(isinstance(assignment_responses, list))
		self.assertEquals(1, len(assignment_responses))
		self.assertTrue(isinstance(assignment_responses[0], dict))
		self.assertEquals(10, assignment_responses[0]['pk'])
		self.assertEquals('Assignment title', assignment_responses[0]['title'])
		self.assertEquals('Assignment text', assignment_responses[0]['text_assignment'])
		self.assertEquals('Competence text', assignment_responses[0]['text_competence'])
		self.assertEquals('Assignment text', assignment_responses[0]['new_text_assignment'])
		self.assertEquals('Competence text', assignment_responses[0]['new_text_competence'])
		self.assertEquals(8, assignment_responses[0]['assignment_pk'])

	def test_callingGetClientResponsesReturnsEmptyStringForTextsIfTheyAreNone(self):
		self.assignment_key_to_user_relation.getResponses = mock.MagicMock()
		self.assignment_key_to_user_relation.getResponses.return_value = [
			AssignmentResponse(
				pk=10,
				assignment=Assignment(pk=8,title='Assignment title'),
				text_assignment=None,
				text_competence=None
				)
		]
		assignment_responses = self.assignment_key_to_user_relation.getClientResponses()
		self.assertEquals('', assignment_responses[0]['text_assignment'])
		self.assertEquals('', assignment_responses[0]['text_competence'])

	def test_callingSaveResponseCallsGetOnAssignmentReponseWithTheExpectedArguments(self):
		AssignmentResponse.objects.get = mock.MagicMock()
		self.assignment_key_to_user_relation.saveResponse(1, 'assignment text 1', 'competence text 1')
		AssignmentResponse.objects.get.assert_any_call(pk=1)

	def test_callingSaveResponseCallsSaveOnAssignmentResponse(self):
		AssignmentResponse.objects.get = mock.MagicMock()
		assignment_response = AssignmentResponse(pk=1, text_assignment='assignment text', text_competence='competence text')
		AssignmentResponse.objects.get.return_value = assignment_response
		AssignmentResponse.objects.get.return_value.save = mock.MagicMock()
		self.assignment_key_to_user_relation.saveResponse(1, 'assignment text 1', 'competence text 1')
		self.assertEquals('assignment text 1', assignment_response.text_assignment)
		self.assertEquals('competence text 1', assignment_response.text_competence)
		self.assertEquals(1, assignment_response.save.call_count)

	def test_callingSaveResponsesCallsSaveResponseOneTimePerAssignmetResponseWithExpectedArguments(self):
		self.assignment_key_to_user_relation.saveResponse = mock.MagicMock()
		self.assignment_key_to_user_relation.saveResponses([dict(id=1, text_assignment='', text_competence=''), dict(id=4, text_assignment='d', text_competence='s')])
		self.assertEquals(2, self.assignment_key_to_user_relation.saveResponse.call_count)
		self.assignment_key_to_user_relation.saveResponse.assert_any_call(1, '', '')
		self.assignment_key_to_user_relation.saveResponse.assert_any_call(4, 'd', 's')

	def setUp(self):
		AssignmentKeyToUserRelation.objects.get = mock.MagicMock()
		AssignmentKeyToUserRelation.objects.get.return_value = AssignmentKeyToUserRelation(pk=876)
		AssignmentResponse.objects.create = mock.MagicMock()
		AssignmentResponse.objects.filter = mock.MagicMock()
		AssignmentResponse.objects.filter.return_value.order_by = mock.MagicMock()
		Assignment.objects.all = mock.MagicMock()
		self.assignments = [Assignment(pk=1), Assignment(pk=3)]
		Assignment.objects.all.return_value = self.assignments
		self.assignment_key_to_user_relation = AssignmentKeyToUserRelation(pk=84)


class CompetenceFieldCollectionToUserRelationTest(unittest.TestCase):

	def test_ExpectThatCompetenceFieldCollectionToUserRelationInstanceHasIsPrivateSetToTruByDefault(self):
		self.competence_field_collection_to_user_relation = CompetenceFieldCollectionToUserRelation()
		self.assertTrue(self.competence_field_collection_to_user_relation.is_private)

	def test_callingToggleIsPrivateInvertsTheIsPrivateProperty(self):
		self.assertTrue(self.competence_field_collection_to_user_relation.is_private)
		self.competence_field_collection_to_user_relation.toggleIsPrivate()
		self.assertFalse(self.competence_field_collection_to_user_relation.is_private)
		self.competence_field_collection_to_user_relation.toggleIsPrivate()
		self.assertTrue(self.competence_field_collection_to_user_relation.is_private)

	def test_callingToogleIsPrivateCallsSaveOnTheCompetenceFieldCollectionToUserRelation(self):
		self.competence_field_collection_to_user_relation.toggleIsPrivate()
		self.assertEquals(1, CompetenceFieldCollectionToUserRelation.save.call_count)

	def setUp(self):
		CompetenceFieldCollectionToUserRelation.save = mock.MagicMock()
		self.competence_field_collection_to_user_relation = CompetenceFieldCollectionToUserRelation()

class AssignmentKeyTest(unittest.TestCase):

	def test_ExpectThatTheModelAssignmentKeyExists(self):
		assignment_key = AssignmentKey()
		self.assertTrue(isinstance(assignment_key, Model))


class AssignmentTest(unittest.TestCase):

	def test_ExpectThatTheModelAssignmentExists(self):
		assignment = Assignment()
		self.assertTrue(isinstance(assignment, Model))


class AssignmentKeyToUserRelationPrivacyTest(unittest.TestCase):

	def test_callingToogleIsPrivateInvertsTheIsPrivateProperty(self):
		self.assertTrue(self.assignment_key_to_user_relation.is_private)
		self.assignment_key_to_user_relation.toggleIsPrivate()
		self.assertFalse(self.assignment_key_to_user_relation.is_private)
		self.assignment_key_to_user_relation.toggleIsPrivate()
		self.assertTrue(self.assignment_key_to_user_relation.is_private)

	def test_callingToogleIsPrivateCallsSaveOnTheAssignmentKeyToUserRelation(self):
		self.assignment_key_to_user_relation.toggleIsPrivate()
		self.assertEquals(1, AssignmentKeyToUserRelation.save.call_count)

	def setUp(self):
		AssignmentKeyToUserRelation.save = mock.MagicMock()
		self.assignment_key_to_user_relation = AssignmentKeyToUserRelation()


class TextMappingTest(unittest.TestCase):

	def test_replaceAllTextAsEmployee(self):
		text = '{Du} {du} {Mentor} {mentor} {Dig} {dig} {Din} {din} {Dine} {dine} {Dit} {dit}'
		expected_text = 'Du du Mentor mentor Dig dig Din din Dine dine Dit dit'
		self.assertEquals(expected_text, replaceAllText(text, True))

	def test_replaceAllTextAsManager(self):
		text = '{Du} {du} {Mentor} {mentor} {Dig} {dig} {Din} {din} {Dine} {dine} {Dit} {dit}'
		expected_text = 'Medarbejderen medarbejderen Medarbejderen medarbejderen Medarbejderen medarbejderen Medarbejderens medarbejderens Medarbejderens medarbejderens Medarbejderens medarbejderens'
		self.assertEquals(expected_text, replaceAllText(text, False))
