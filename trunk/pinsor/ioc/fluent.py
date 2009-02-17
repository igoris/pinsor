from registration import *
from components import *
from enums import *


class FluentService(object):

	def __init__(self):
		self.GraphNode = None
				
	def Named(self, key):
		self.GraphNode.Key = key
		return self
	
	def Depends(self, dependtuple):
		self.GraphNode.Component.Depends = dependtuple
		return self
	
	def LifeStyle(self, lifestyle):
		self.GraphNode.Component.LifeStyle = lifestyle
		return self
		
class Component(object):
	
	@staticmethod			
	def For(cls):
		fluent  = FluentService()
		fluent.GraphNode = GraphNode(key=cls.__name__, component=ComponentModel(classtype=cls, depends=[], lifestyle = LifeStyle.Singleton()) )
		return fluent
		


