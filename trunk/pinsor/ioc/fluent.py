from registration import *
from components import *
from enums import *


class FluentService(object):

	def __init__(self):
		self.ComponentModel = None
				
	def Named(self, key):
		self.ComponentModel.Key = key
		return self
	
	def Depends(self, dependtuple):
		self.ComponentModel.Component.Depends = dependtuple
		return self
	
	def LifeStyle(self, lifestyle):
		self.ComponentModel.Component.LifeStyle = lifestyle
		return self
		
class Service(object):
	
	@staticmethod			
	def For(cls):
		fluent  = FluentService()
		fluent.ComponentModel = ComponentModel(key=cls.__name__, component=Component(classtype=cls, depends=[], lifestyle = LifeStyle.Singleton()) )
		return fluent
		


