# from models import Company, CompetenceFieldCollectionToCompanyRelation, CompetenceFieldCollection
# from models import Employee, CompetenceFieldCollectionToUserRelation, QuestionResponse, Question
# from models import Competence, CompetenceField, CompetenceQuestion
# from django.contrib.auth.models import User
# import datetime
# from types import MethodType


# class CompanyMock(Company):
# def __init__(self, *args, **kwargs):
# self.competence_field_collection_to_company_relations = list()
#         Company.__init__(self, *args, **kwargs)

#     def addCompetenceFieldCollectionToCompanyRelation(self, competence_field_collection_to_company_relation):
#         competence_field_collection_to_company_relation.competence_field_collection = CompetenceFieldCollection()
#         self.competence_field_collection_to_company_relations.append(
#             competence_field_collection_to_company_relation
#         )

#     def getAvailableSchemes(self):
#         original_filter = CompetenceFieldCollectionToCompanyRelation.objects.filter
#         try:
#             def filterMock(*args, **kwargs):
#                 return self.competence_field_collection_to_company_relations

#             CompetenceFieldCollectionToCompanyRelation.objects.filter = filterMock
#             return Company.getAvailableSchemes(self)
#         finally:
#             CompetenceFieldCollectionToCompanyRelation.objects.filter = original_filter


# class MockedList(list):
#     pk = 1
#     finished_at = None
#     created_at = datetime.datetime.now()
#     competence_field_collection = list()
#     def order_by(self, *args, **kwargs):
#         return self

#     def exclude(self, *args, **kwargs):
#         return self


# class EmployeeMock(Employee):
#     def __init__(self, *args, **kwargs):
#         self.competence_field_collection_to_user_relations = MockedList()
#         self.employees = list()
#         Employee.__init__(self, *args, **kwargs)

#     def addCompetenceFieldCollectionToUserRelation(self, competence_field_collection_to_user_relation):
#         competence_field_collection_to_user_relation.competence_field_collection = CompetenceFieldCollection()
#         self.competence_field_collection_to_user_relations.append(
#             competence_field_collection_to_user_relation
#         )

#     def getSchemes(self, my_own = None):
#         original_filter = CompetenceFieldCollectionToUserRelation.objects.filter
#         original_employee_filter = Employee.objects.filter
#         try:
#             def filterMock(*args, **kwargs):
#                 if kwargs.has_key('user__pk__in'):
#                     relations = MockedList()
#                     for employee in self.employees:
#                         if employee.user.pk in kwargs.get('user__pk__in'):
#                             relations.append(employee.competence_field_collection_to_user_relations)
#                     return relations
#                 else:
#                     return self.competence_field_collection_to_user_relations

#             class EmployeeFilterMock():
#                 def __init__(self, *args, **kwargs):
#                     self.employees = kwargs.get('employees')

#                 def values_list(self, *args, **kwargs):
#                     ids = list()
#                     for employee in self.employees:
#                         ids.append(employee.pk)
#                     return ids

#             def employeeFilter(*args, **kwargs):
#                 return EmployeeFilterMock(employees = self.employees)

#             Employee.objects.filter = employeeFilter
#             CompetenceFieldCollectionToUserRelation.objects.filter = filterMock
#             return Employee.getSchemes(self, my_own)
#         finally:
#             CompetenceFieldCollectionToUserRelation.objects.filter = original_filter
#             Employee.objects.filter = original_employee_filter

#     def getQuestionnaire(self, competence_field_collection_to_user_relation_id):
#         original_get = CompetenceFieldCollectionToUserRelation.objects.get
#         try:
#             def getMock(*args, **kwargs):
#                 if len(self.competence_field_collection_to_user_relations) > 0:
#                     return self.competence_field_collection_to_user_relations[0]
#                 return type('A', (object,),
#                             {
#                                 'competence_field_collection': None,
#                                 'pk': 0,
#                                 'finished_at': None
#                             }
#                 )

#             CompetenceFieldCollectionToUserRelation.objects.get = getMock
#             return Employee.getQuestionnaire(self, competence_field_collection_to_user_relation_id)
#         finally:
#             CompetenceFieldCollectionToUserRelation.objects.get = original_get

#     def addEmployee(self, employee):
#         employee.manager = self
#         self.employees.append(employee)


# class CompetenceFieldCollectionToUserRelationMock(CompetenceFieldCollectionToUserRelation):
#     def __init__(self, *args, **kwargs):
#         CompetenceFieldCollectionToUserRelation.__init__(self, args, kwargs)
#         self.question_responses = list()
#         self.questions = list()
#         self.collection = list()

#     def addQuestionAndResponseToCollection(self, question_id, answer_text = None):
#         question = self.addQuestion(question_id, 'question title')
#         if answer_text is None:
#             question_response = QuestionResponse()
#             question_response.pk = 10
#             question_response.competence_field_collection_to_user_relation = self
#             question_response.question = question
#             question_response.text = answer_text
#         competence_field_collection = CompetenceFieldCollectionMock()
#         competence_field_collection.addQuestionToCollection(question)
#         self.collection.append(competence_field_collection)

#     def addQuestionResponse(self, question_id, answer_text):
#         question_response = QuestionResponse()
#         question_response.pk = 10
#         question_response.competence_field_collection_to_user_relation = self
#         question_response.question = self.addQuestion(question_id, 'question title')
#         question_response.text = answer_text
#         self.question_responses.append(question_response)
#         return question_response

#     def addQuestion(self, question_id, title):
#         question = Question(title=title)
#         question.pk = question_id
#         self.questions.append(question)
#         return question

#     def getQuestionResponses(self, respect_finished_at=None):
#         original_related = CompetenceFieldCollectionToUserRelation\
#             .question_response_competence_field_collection_to_user_relation
#         original_collection = CompetenceFieldCollectionToUserRelation.competence_field_collection
#         try:
#             class RelatedMock():
#                 def __init__(self, *args, **kwargs):
#                     self.question_responses = kwargs.get('question_responses')

#                 def all(self):
#                     return self.question_responses

#                 def get(self, *args, **kwargs):
#                     if not kwargs.has_key('question__pk'):
#                         return None
#                     for question_response in self.question_responses:
#                         if question_response.question.pk == kwargs.get('question__pk'):
#                             return question_response
#                     return None

#             class CollectionMock():
#                 def __init__(self, *args, **kwargs):
#                     self.questions = kwargs.get('questions')
#                 def getQuestions(self):
#                     return self.questions

#                 #def get(self, *args, **kwargs):
#                 #    pass

#             CompetenceFieldCollectionToUserRelation.\
#                 question_response_competence_field_collection_to_user_relation = \
#                 RelatedMock(question_responses=self.question_responses)
#             CompetenceFieldCollectionToUserRelation.competence_field_collection = \
#                 CollectionMock(questions=self.questions)
#             return CompetenceFieldCollectionToUserRelation.getQuestionResponses(self, respect_finished_at)
#         finally:
#             CompetenceFieldCollectionToUserRelation.question_response_competence_field_collection_to_user_relation = \
#                 original_related
#             CompetenceFieldCollectionToUserRelation.competence_field_collection = original_collection

#     def getCompetenceFieldCollectionQuestions(self):
#         original_collection = CompetenceFieldCollectionToUserRelation.competence_field_collection
#         try:
#             #CompetenceFieldCollectionToUserRelation.competence_field_collection = self.collection
#             return CompetenceFieldCollectionToUserRelation.getCompetenceFieldCollectionQuestions(self)
#         finally:
#             CompetenceFieldCollectionToUserRelation.competence_field_collection = original_collection



# class CompetenceMock(Competence):
#     def __init__(self, *args, **kwargs):
#         Competence.__init__(self, *args, **kwargs)


# class CompetenceFieldMock(CompetenceField):
#     def __init__(self, *args, **kwargs):
#         CompetenceField.__init__(self, *args, **kwargs)

#     def addQuestion(self, question):
#         self.questions.append(question)


# class CompetenceFieldCollectionMock(CompetenceFieldCollection):
#     def __init__(self, *args, **kwargs):
#         CompetenceFieldCollection.__init__(self, *args, **kwargs)

#     def addQuestion(self, question):
#         self.competence_fields[0].addQuestion(question)

#     def addQuestionToCollection(self, question):
#         self.competence_fields


# class CreateGetMock():
#     def __init__(self, *args, **kwargs):
#         self._objects = list()

#     def getMock(self, *args, **kwargs):
#         if len(self._objects) > 0:
#             for obj in self._objects:
#                 if obj.user.pk == kwargs.get('user__pk'):
#                     return obj
#         return None

#     def createMock(self, *args, **kwargs):
#         competence_field_collection_to_user_collection = CompetenceFieldCollectionToUserRelation()
#         competence_field_collection_to_user_collection.user = kwargs.get('user')
#         competence_field_collection_to_user_collection.competence_field_collection = kwargs.get(
#             'competence_field_collection'
#         )
#         self._objects.append(competence_field_collection_to_user_collection)
#         return competence_field_collection_to_user_collection


# class AllMock():

#     def __init__(self, *args, **kwargs):
#         self._objects = list()

#     def append(self, obj):
#         self._objects.append(obj)

#     def all(self):
#         return self._objects

#     def __getitem__(self, item):
#         return self._objects[item]

#     def getQuestions(self):
#         print 'hej'
#         return self.all()


# class MethodCalledOnceMock():
#     def __init__(self, *args, **kwargs):
#         self._called = False

#     def methodMock(self, *args, **kwargs):
#         self._called = True

#     def getCalled(self):
#         return self._called

#     def methodStub(self):
#         pass

# class MethodCalledNoTimesMock():
#     def __init__(self, *args, **kwargs):
#         self._called = 0

#     def methodMock(self, *args, **kwargs):
#         self._called += 1

#     def getCalled(self):
#         return self._called

# class CreateQuestionResponseMock(MethodCalledOnceMock):
#     def __init__(self, *args, **kwargs):
#         MethodCalledOnceMock.__init__(self, *args, **kwargs)
#         self.exists_return_value = False

#     def setExistsReturnValue(self, value):
#         self.exists_return_value = value

#     def create(self, *args, **kwargs):
#         self.methodMock()
#         self.question_response = QuestionResponse(
#             question=kwargs.get('question'),
#             competence_field_collection_to_user_relation=kwargs.get('competence_field_collection_to_user_relation'),
#             text=kwargs.get('text'),
#             created_by=kwargs.get('created_by'),
#             updated_by=kwargs.get('updated_by')
#         )
#         return self.question_response

#     def filter(self, *args, **kwargs):
#         class ExistsMock():
#             def __init__(self, *args, **kwargs):
#                 self.exists_return_value = kwargs.get('exists_return_value')
#                 self.dict = {
#                     'pk': 1,
#                     'text': 'old answer text'
#                 }
#             def exists(self):
#                 return self.exists_return_value
#         return ExistsMock(exists_return_value = self.exists_return_value)

#     def save(self):
#         pass

#     def getQuestionResponse(self, *args, **kwargs):
#         if self.exists_return_value:
#             return self.question_response
#         return QuestionResponse()

#     def getQuestion(self, *args, **kwargs):
#         return Question(
#             pk = kwargs.get('pk')
#         )
