#from pinsor import *
from tests.utility import *
import unittest

class Container_tests:
	def setUp(self):
		self.pinsor = PinsorContainer()
				
	def test_can_store_and_register_by_class_type(self):
		self.pinsor.AddComponent(FakeObj)		
		fake1 = self.pinsor.Resolve(FakeObj)
		assert isinstance(fake1, FakeObj)
		
	def test_can_store_and_register_by_key(self):
		self.pinsor.AddComponent(FakeObj, key="fake1")
		fake1 = self.pinsor.Resolve(key="fake1")
		assert isinstance(fake1, FakeObj)
		
	def test_can_store_with_key_and_retrieve_by_class_type_when_only_one_class_is_registered(self):
		self.pinsor.AddComponent(FakeObj, key="fake1")
		fake1 = self.pinsor.Resolve(FakeObj)
		assert isinstance(fake1, FakeObj)
		
class ContainerWhenResolvingDependenciesStoredByClassName_tests(unittest.TestCase):
	
	def setUp(self):
		self.pinsor = PinsorContainer()
		self.pinsor.AddComponent(NeedsFakeObj,depends=[FakeObj])
		self.pinsor.AddComponent(FakeObj)
		
	def test_can_automatically_retrieve_dependencies_when_resolve_is_called(self):
		needsfake = self.pinsor.Resolve(NeedsFakeObj)
		instance = needsfake.FakeInstance()
		print instance
		result = isinstance(instance, FakeObj)
		assert result
		
	def test_should_throw_error_when_dependency_has_not_been_found_in_graph(self):
		try:
			needsfake = self.pinsor.Resolve(FakeObjWithArgs)
			assert falsepass
		except NotFoundInObjectGraphError:
			pass
			
		

class ContainerWhenResolvingDependenciesStoredByKey_tests(unittest.TestCase):
	def setUp(self):
		self.pinsor = PinsorContainer()
		self.pinsor.AddComponent(NeedsFakeObj, depends=[Config("fake1")], key="needs1")
		self.pinsor.AddComponent(FakeObj, key="fake1")
		
	def test_can_automatically_retrieve_dependencies_when_resolve_is_called_by_type(self):
		fake1 = self.pinsor.Resolve(NeedsFakeObj)
		self.assertTrue(isinstance(fake1,NeedsFakeObj))
		self.assertTrue(isinstance(fake1.FakeInstance(), FakeObj))

	def test_can_automatically_retrieve_dependencies_when_resolve_is_called_by_key(self):
		fake1 = self.pinsor.Resolve(key="needs1")
		self.assertTrue(isinstance(fake1,NeedsFakeObj))
		self.assertTrue(isinstance(fake1.FakeInstance(), FakeObj))
		
	def test_should_throw_error_when_dependency_has_not_been_found_in_graph(self):
		try:
			needsfake = self.pinsor.Resolve(key="nokey")
			assert falsepass
		except KeyError:
			pass
		
class ContainerWhenResolvingDependenciesStoredByInstance_tests(object):
	def setUp(self):
		"""docstring for setUp"""
		self.pinsor = PinsorContainer()
		fake1 = FakeObj()
		self.pinsor.AddComponent(NeedsFakeObj, depends=[Instance(fake1)])
		
	def test_can_automatically_retrieve_dependencies_when_resolve_is_called(self):
		needs = self.pinsor.Resolve(NeedsFakeObj)
		assert isinstance(needs, NeedsFakeObj)
		instance = needs.FakeInstance()
		assert isinstance(instance, FakeObj)
	