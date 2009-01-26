from utility import *
from pinsor.ioc import *
import unittest

class test_container(unittest.TestCase):

	def setUp(self):
		self.pinsor = PinsorContainer()
		self.pinsor.AddComponent(FakeObj)

	def test_should_retrieve_class_instantiated(self):
		fakeinstance  = self.pinsor.Resolve(FakeObj)
		assert isinstance(fakeinstance, FakeObj)

	def test_should_build_class_with_one_dependency(self):
		self.pinsor.AddComponent(NeedsFakeObj, depends=[FakeObj])
		needsfake = self.pinsor.Resolve(NeedsFakeObj)
		assert isinstance(needsfake, NeedsFakeObj)
		assert needsfake.HasFakeObj()

	def test_should_instantiate_all_objects_in_dependency_tree(self):
		self.pinsor.AddComponent(NeedsFakeObj, depends=[FakeObj])
		self.pinsor.AddComponent(FakeObjWithArgs, depends=[FakeObj, NeedsFakeObj])
		fakeobj = self.pinsor.Resolve(FakeObjWithArgs)
		assert isinstance(fakeobj, FakeObjWithArgs)
		assert fakeobj.DoesStuff()


class test_inspector_when_getting_arg_count(unittest.TestCase):


	def setUp(self):
		self.inspect = Inspector()

	def test_should_get_arg_coun(self):
		def func(a, b,c,d):
			pass
		count = self.inspect.get_arg_count(func)
		assert 4 == count

	def test_should_return_0_when_no_args_found_on_method(self):
		def func():
			pass
		count = self.inspect.get_arg_count(func)
		assert 0 == count


class test_inspector_when_building_class(unittest.TestCase):

	def setUp(self):
		self.inspect = Inspector()

	def test_should_build_class_with_no_dependencies(self):
		fakeobj = self.inspect.build_class(FakeObj, [])
		assert isinstance(fakeobj, FakeObj)

	def test_should_build_class_with_dependencies_passed_to_init(self):
		fakeobj = FakeObj()
		needsfake = self.inspect.build_class(NeedsFakeObj, [fakeobj])
		assert isinstance(needsfake, NeedsFakeObj)
