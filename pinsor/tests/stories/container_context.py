from pinsor.tests.utility import FakeObj, NeedsFakeObj, FakeObjWithArgs
from pinsor.ioc.container import PinsorContainer
from pinsor.ioc.enums import LifeStyle
from pinsor.ioc.registration import Config
import unittest


class container_tests(unittest.TestCase):

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
    
    def test_should_retrieve_dependencies_dependencies_by_key(self):
        pinsor = PinsorContainer()
        pinsor.AddComponent(FakeObj, key="comp.fakeobj")
        pinsor.AddComponent(NeedsFakeObj, depends = [Config("comp.fakeobj")])
        needsfake = pinsor.Resolve(NeedsFakeObj)
        assert needsfake.HasFakeObj
        
class container_when_registering_more_than_one_of_the_same_class_with_different_keys_tests(unittest.TestCase):
    
    def test_should_return_different_instances(self):
        pinsor = PinsorContainer()
        pinsor.AddComponent(FakeObj, key="comp.fake1")
        pinsor.AddComponent(FakeObj, key="comp.fake2")
        fake1 = pinsor.Resolve(key="comp.fake1")
        fake2 = pinsor.Resolve(key="comp.fake2")
        self.assertNotEqual(id(fake1), id(fake2))
        
