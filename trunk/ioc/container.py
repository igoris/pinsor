import functools

def compare_cls(clsa, clsb):
	acount = get_arg_count(clsa.__init__)
	bcount = get_arg_count(clsb.__init__)
	return cmp(acount,bcount)

class Inspector(object):
	def get_arg_count(self,func):
		code = func.func_code
		argcount = code.co_argcount
		return argcount
		
	def bldcls(self,cls, dep):
		if len(dep) == 0:
			return cls()
		return cls(*dep)

class Resolver(object):
	
	def __init__(self, inspect = Inspector()):
		self.__inspect = inspect
		
	def walk(self,graph,cls):
		for o, d in graph.iteritems():
			if o == cls:
				deps = []
				if d > 0:
					for dep in d:
						deps.append(self.walk(graph, dep))
				obj = self.__inspect.bldcls(cls, deps)
				return obj
	
		
	
class PinsorContainer(object):
	
	def __init__(self, resolver = Resolver()):
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
		
