from pinsor.ioc.container import DefaultResolver, PinsorContainer
from pinsor.ioc.registration import Config, Instance
from pinsor.ioc.components import GraphNode, ComponentModel
from pinsor.ioc.fluent import FluentService, Component
from pinsor.ioc.enums import LifeStyle
from pinsor.tests.utility import FakeObj, NeedsFakeObj, FakeObjWithArgs
import unittest 
        
class fluent_registration_of_objects_tests(unittest.TestCase):
    
    def setUp(self):
        self.pinsor = PinsorContainer()
        
    def test_should_take_pass_component_into_containter_by_class_name(self):
        self.pinsor.Register(Component.oftype(FakeObj))
        fake = self.pinsor.Resolve(FakeObj)
        assert isinstance(fake,FakeObj)
    
    def test_should_take_pass_component_into_container_and_set_key(self):
        self.pinsor.Register(Component.oftype(FakeObj).named("comp.key"))
        assert self.pinsor.ObjectGraph["comp.key"].ClassType == FakeObj
        fake = self.pinsor.Resolve(key='comp.key');
        assert isinstance(fake, FakeObj)    
    
    def test_should_pass_more_than_one_component_into_container(self):
        self.pinsor.Register(
                            Component.oftype(FakeObj).named("fake1"),
                            Component.oftype(FakeObj).named("fake2")
                             )
        fake1 = self.pinsor.Resolve(key="fake1")
        fake2 = self.pinsor.Resolve(key="fake2")
        assert isinstance(fake1, FakeObj)
        assert isinstance(fake2, FakeObj)
        
    def test_should_set_dependencies(self):
        self.pinsor.Register(
                            Component.oftype(FakeObj),
                            Component.oftype(NeedsFakeObj).depends([FakeObj])
                            )
        needsfake = self.pinsor.Resolve(NeedsFakeObj)
        assert needsfake.HasFakeObj()
    
    def test_should_set_lifestyle(self):
        self.pinsor.Register(
                             Component.oftype(FakeObj).lifestyle(LifeStyle.Transient())\
                             )
        fake1 = self.pinsor.Resolve(FakeObj)
        fake2 = self.pinsor.Resolve(FakeObj)
        self.assertNotEqual(id(fake1), id(fake2))
        
    def test_should_set_multiple_options_at_once(self):
        self.pinsor.Register(
                            Component.oftype(FakeObj),
                            Component.oftype(NeedsFakeObj).depends([FakeObj]).named("needs").lifestyle(LifeStyle.Transient())
                            )
        com = self.pinsor.ObjectGraph["needs"]
        self.assertEqual(NeedsFakeObj, com.ClassType)
        self.assertEqual("transient", com.LifeStyle)
        self.assertEqual(FakeObj, com.Depends[0])
        
    def test_should_be_able_to_register_by_key(self):
        self.pinsor.Register(
                            Component.oftype(FakeObj).named("fake1"),
                            Component.oftype(FakeObj).named("fake2"),
                            Component.oftype(NeedsFakeObj).depends([Config("fake1")]).named("needs1"),
                            Component.oftype(NeedsFakeObj).depends([Config("fake2")]).named("needs2")
                            )
        fake2_id = id(self.pinsor.Resolve(key="fake2"))
        needsfake = self.pinsor.Resolve(key="needs2")
        fakefromneeds1_id = id(needsfake.FakeInstance())
        
    def test_should_be_able_register_a_param(self):
        fakeobj = FakeObj()
        self.pinsor.Register(
                            Component.oftype(NeedsFakeObj).depends([Instance(fakeobj)])
                            )
                            
        fakefromneeds = self.pinsor.Resolve(NeedsFakeObj)
        self.assertEqual(id(fakeobj), id(fakefromneeds.FakeInstance()))