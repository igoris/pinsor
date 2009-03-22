"""Stub classes used for testing"""
class FakeObj(object):
    """Has no dependencies"""
    @property
    def Name(self):
        return self.__name
    
    def __init__(self, name= "empty"):
        self.__name = name
        
    def Command(self):
        """docstring for Command"""
        pass
        
class NeedsFakeObj(object):
    """has one dependency on FakeObj"""
    def __init__(self, fakeObj):
        self.__fake_obj = fakeObj
        
    def FakeInstance(self):
        return self.__fake_obj
            
    def HasFakeObj(self):
        return isinstance(self.__fake_obj, FakeObj)

class FakeObjWithArgs(object):
    """has two dependencies of fakeobj"""
    def __init__(self, fakeobj, object):
        self.__fakeobj = fakeobj
        self.__object = object
        
    def DoesStuff(self):
        return isinstance(self.__fakeobj, FakeObj)
        
class CircularDependencyA(object):
    def __init__(self, dependencyB):
        self.dependencyB = dependencyB

class CircularDependencyB(object):
    def __init__(self, dependencyA):
        self.dependencyA = dependencyA
