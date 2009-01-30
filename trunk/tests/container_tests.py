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
	
	def test_should_return_same_instance_each_time_resolve_is_called_by_default(self):
		fakeobj1 = self.pinsor.Resolve(FakeObj)
		fakeobj2 = self.pinsor.Resolve(FakeObj)
		self.assertEqual(id(fakeobj1), id(fakeobj2))
	
	def test_should_return_new_instance_each_time_resolve_is_called_when_lifestyle_of_that_component_is_set_to_transient(self):
		pinsor = PinsorContainer()
		pinsor.AddComponent(FakeObj, depends=[], lifestyle = LifeStyle.Transient)
		fakeobj1 = pinsor.Resolve(FakeObj)
		fakeobj2 = pinsor.Resolve(FakeObj)
		assert isinstance(fakeobj1, FakeObj)
		assert isinstance(fakeobj2, FakeObj)
		self.assertNotEqual(id(fakeobj1), id(fakeobj2))
		
	def test_should_be_able_to_resolve_by_component_key(self):
		pinsor = PinsorContainer()
		pinsor.AddComponent(FakeObj, key="comp.fakeobj")
		fakeobj = pinsor.Resolve(key="comp.fakeobj")
		assert isinstance(fakeobj, FakeObj)
	
	def test_should_retrieve_dependencies_by_key(self):
		pinsor = PinsorContainer()
		pinsor.AddComponent(FakeObj, key="comp.fakeobj")
		pinsor.AddComponent(NeedsFakeObj, depends = [Config("comp.fakeobj")])
		needsfake = pinsor.Resolve(NeedsFakeObj)
		assert needsfake.HasFakeObj
		
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

class test_inspector_when_retrieving_class_tuple_from_graph(unittest.TestCase):

	def setUp(self):
		self.inspect = Inspector()
		self.graph = {}
		self.graph["comp.FakeObj"] = Component(FakeObj, [], LifeStyle.Transient)
		
	def test_should_retrieve_tuple_class_already_in_object_graph_by_type(self):
		cls = self.inspect.get_class_tuple_from_graph(self.graph, FakeObj, None)
		assert cls[0] == "comp.FakeObj"
		comp = cls[1]
		assert comp.ClassType == FakeObj
		
	def test_when_more_than_one_of_same_type_in_graph_should_retrieve_tuple_class_already_in_object_graph_by_key(self):
		self.graph["comp.FakeObj2"] = Component(FakeObj, [], LifeStyle.Transient)
		cls = self.inspect.get_class_tuple_from_graph(self.graph, FakeObj, "comp.FakeObj2")
		assert cls[0] == "comp.FakeObj2"
		comp = cls[1]
		assert comp.ClassType == FakeObj
