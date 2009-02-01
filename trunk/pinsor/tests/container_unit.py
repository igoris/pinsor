from utility import *
from pinsor.ioc import *
import unittest


class test_builder_when_building_class(unittest.TestCase):

	def setUp(self):
		self.inspect = Builder()

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
		cls = self.inspect.find_class_by_key_or_class(self.graph, FakeObj, None)
		assert cls.Key == "comp.FakeObj"
		comp = cls.Component
		assert comp.ClassType == FakeObj
		
	def test_when_more_than_one_of_same_type_in_graph_should_retrieve_tuple_class_already_in_object_graph_by_key(self):
		self.graph["comp.FakeObj2"] = Component(FakeObj, [], LifeStyle.Transient)
		cls = self.inspect.find_class_by_key_or_class(self.graph, FakeObj, "comp.FakeObj2")
		assert cls.Key == "comp.FakeObj2"
		comp = cls.Component
		assert comp.ClassType == FakeObj
		
class test_DefaultLifeStyleResolver_when_using_singleton(unittest.TestCase):
	
	def setUp(self):
		self.instances = {}
		self.resolvedobj = FakeObj()
		self.resolver = DefaultLifeStyleResolver()
		
	def test_should_store_obj_in_instances_when_lifestyle_is_set_to_singleton(self):
		self.resolver.handle_lifestyle(LifeStyle.Singleton(), self.instances,self.resolvedobj ,FakeObj)
		assert self.resolvedobj in self.instances.values()
	
	def test_should_not_store_obj_in_instances_if_life_style_is_transient(self):
		self.resolver.handle_lifestyle(LifeStyle.Transient(), self.instances, self.resolvedobj, FakeObj)
		assert self.resolvedobj not in self.instances.values()

class test_Searcher(unittest.TestCase):
	
	def setUp(self):
		self.searcher = Searcher()
	
	def test_should_match_by_class_type_regardless_of_key(self):
		graph = {}
		graph["compkey"] = Component( FakeObj ,[] , LifeStyle.Singleton())
		graph["FakeObj"] = Component(FakeObj, [], LifeStyle.Transient())
		match = self.searcher.match_by_class(graph, FakeObj)
		self.assertEqual(2, len(match))
					
	def test_should_match_by_string_key(self):
		objary = []
		objary.append(("compkey",Component(FakeObj, [], LifeStyle.Singleton())))
		objary.append(("otherkey", Component(FakeObj, [], LifeStyle.Singleton())))
		match = self.searcher.match_by_key(objary, "compkey")
		assert match is not None
		assert match[0] == "compkey"