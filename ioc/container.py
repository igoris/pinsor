from enums import *


class Inspector(object):
		
	def build_class(self,cls, dep):
		if len(dep) == 0:
			return cls()
		return cls(*dep)

class DefaultResolver(object):
	
	def __init__(self, inspect = Inspector()):
		self.__inspect = inspect
		
	def walk(self,graph,cls,instances):
		if cls in instances:
			return instances[cls] 
		for o, d in graph.iteritems():
			if o == cls:
				deps = []
				if d[0] > 0:
					for dep in d[0]:
						deps.append(self.walk(graph, dep,instances))
				obj = self.__inspect.build_class(cls, deps)
				if d[1] == "singleton":
					instances[cls] = obj
				return obj
	
		
	
class PinsorContainer(object):
	
	def __init__(self, resolver = DefaultResolver()):
		self.__objectgraph = {}
		self.__instances = {}
		self.__resolver = resolver
		
	def AddComponent(self,type, depends = [], lifestyle = LifeStyle.Singleton()):
		self.__objectgraph[type] = [depends, lifestyle]
			
	def Resolve(self,type):
		obj = self.__resolver.walk(self.__objectgraph, type, self.__instances)
		return obj

	@property
	def ObjectGraph(self):	
		return self.__objectgraph
		