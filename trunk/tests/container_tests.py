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
