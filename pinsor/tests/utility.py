from pinsor.ioc import *


class FakeObj(object):
	
	@property
	def Name(self):
		return self.__name
	
	def __init__(self, name= "empty"):
		self.__name = name
		
	def Command(self):
		"""docstring for Command"""
		pass
		
class NeedsFakeObj(object):
	
	def __init__(self, fakeObj):
		self.__fake_obj = fakeObj
		
	def FakeInstance(self):
		return self.__fake_obj
			
	def HasFakeObj(self):
		return isinstance(self.__fake_obj, FakeObj)

class FakeObjWithArgs(object):
	
	def __init__(self, fakeobj, object):
		self.__fakeobj = fakeobj
		self.__object = object
		
	def DoesStuff(self):
		return isinstance(self.__fakeobj, FakeObj)