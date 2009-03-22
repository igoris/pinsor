from pinsor.tests.utility import FakeObj, NeedsFakeObj, FakeObjWithArgs, CircularDependencyA, CircularDependencyB
from pinsor.ioc.container import PinsorContainer
from pinsor.ioc.enums import LifeStyle
from pinsor.ioc.registration import Config
from pinsor.ioc.exceptions import CircularDependencyException
import unittest


class container_tests(unittest.TestCase):

    def setUp(self):
        self.pinsor = PinsorContainer()
        self.pinsor.addcomponent(FakeObj)

    def test_should_retrieve_class_instantiated(self):
        fakeinstance  = self.pinsor.resolve(FakeObj)
        assert isinstance(fakeinstance, FakeObj)

    def test_should_build_class_with_one_dependency(self):
        self.pinsor.addcomponent(NeedsFakeObj, depends=[FakeObj])
        needsfake = self.pinsor.resolve(NeedsFakeObj)
        assert isinstance(needsfake, NeedsFakeObj)
        assert needsfake.HasFakeObj()

    def test_should_instantiate_all_objects_in_dependency_tree(self):
        self.pinsor.addcomponent(NeedsFakeObj, depends=[FakeObj])
        self.pinsor.addcomponent(FakeObjWithArgs, depends=[FakeObj, NeedsFakeObj])
        fakeobj = self.pinsor.resolve(FakeObjWithArgs)
        assert isinstance(fakeobj, FakeObjWithArgs)
        assert fakeobj.DoesStuff()
    
    def test_should_return_same_instance_each_time_resolve_is_called_by_default(self):
        fakeobj1 = self.pinsor.resolve(FakeObj)
        fakeobj2 = self.pinsor.resolve(FakeObj)
        self.assertEqual(id(fakeobj1), id(fakeobj2))
    
    def test_should_return_new_instance_each_time_resolve_is_called_when_lifestyle_of_that_component_is_set_to_transient(self):
        pinsor = PinsorContainer()
        pinsor.addcomponent(FakeObj, depends=[], lifestyle = LifeStyle.transient)
        fakeobj1 = pinsor.resolve(FakeObj)
        fakeobj2 = pinsor.resolve(FakeObj)
        assert isinstance(fakeobj1, FakeObj)
        assert isinstance(fakeobj2, FakeObj)
        self.assertNotEqual(id(fakeobj1), id(fakeobj2))
        
    def test_should_be_able_to_resolve_by_component_key(self):
        pinsor = PinsorContainer()
        pinsor.addcomponent(FakeObj, key="comp.fakeobj")
        fakeobj = pinsor.resolve(key="comp.fakeobj")
        assert isinstance(fakeobj, FakeObj)
    
    def test_should_retrieve_dependencies_dependencies_by_key(self):
        pinsor = PinsorContainer()
        pinsor.addcomponent(FakeObj, key="comp.fakeobj")
        pinsor.addcomponent(NeedsFakeObj, depends = [Config("comp.fakeobj")])
        needsfake = pinsor.resolve(NeedsFakeObj)
        assert needsfake.HasFakeObj
    
    def test_should_throw_an_exception_when_circular_dependency_is_found(self):
        pinsor = PinsorContainer()
        pinsor.addcomponent(CircularDependencyA, depends=[CircularDependencyB])
        pinsor.addcomponent(CircularDependencyB, depends=[CircularDependencyA])
        try:
            depA = pinsor.resolve(CircularDependencyA)
        except CircularDependencyException:
            pass
        else:
            self.fail("This should raise an exception")

        
class container_when_registering_more_than_one_of_the_same_class_with_different_keys_tests(unittest.TestCase):
    
    def test_should_return_different_instances(self):
        pinsor = PinsorContainer()
        pinsor.addcomponent(FakeObj, key="comp.fake1")
        pinsor.addcomponent(FakeObj, key="comp.fake2")
        fake1 = pinsor.resolve(key="comp.fake1")
        fake2 = pinsor.resolve(key="comp.fake2")
        self.assertNotEqual(id(fake1), id(fake2))
        
