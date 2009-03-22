#!/usr/bin/env python
# encoding: utf-8
"""
tests the ComponentSet in a unit fashion
"""
from pinsor.ioc.enums import LifeStyle
from pinsor.ioc.components import ComponentModel, ComponentSet
from pinsor.tests.utility import FakeObj
from pinsor.ioc.exceptions import AttemptToAddDuplicateComponentModelToVisitedSet
import unittest

class componentset_storing_test(unittest.TestCase):
    """context: when storing components"""
    
    def test_should_prevent_storing_duplicate_attributes_of_componentmodel(self):
        componentset = ComponentSet()
        componentinstance = ComponentModel(FakeObj, [], LifeStyle.transient())
        componentinstance2nd = ComponentModel(FakeObj, [], LifeStyle.transient())
        componentset.add(componentinstance)
        try:
            componentset.add(componentinstance2nd)
            self.fail("should not happen")
        except AttemptToAddDuplicateComponentModelToVisitedSet:
            pass
        
class componentset_checking_test(unittest.TestCase):
    """context: when checking for the existence of components"""
            
    def test_should_find_components_with_same_attributes_in_list(self):
        componentinstance = ComponentModel(FakeObj, [], LifeStyle.transient())
        componentinstance2nd = ComponentModel(FakeObj, [], LifeStyle.transient())
        componentset = ComponentSet()
        componentset.add(componentinstance)
        assert componentset.has_comp(componentinstance2nd)



