import functools


class Inspector(object):
	def get_arg_count(self,func):
		code = func.func_code
		argcount = code.co_argcount
		return argcount
		
	def build_class(self,cls, dep):
		if len(dep) == 0:
			return cls()
		return cls(*dep)

class DefaultResolver(object):
	
	def __init__(self, inspect = Inspector()):
		self.__inspect = inspect
		
	def walk(self,graph,cls):
		for o, d in graph.iteritems():
			if o == cls:
				deps = []
				if d > 0:
					for dep in d:
						deps.append(self.walk(graph, dep))
				obj = self.__inspect.build_class(cls, deps)
				return obj
	
		
	
class PinsorContainer(object):
	
	def __init__(self, resolver = DefaultResolver()):
		self.__objectgraph = {}
		self.__instances = []
		self.__resolver = resolver
		
	def AddComponent(self,type, depends = []):
		self.__objectgraph[type] = depends
			
	def Resolve(self,type):
		obj = self.__resolver.walk(self.__objectgraph, type)
		return obj

	@property
	def ObjectGraph(self):	
		return self.__objectgraph
		