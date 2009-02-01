from enums import *
from registration import *

class Component(object):
	
	def __init__(self, classtype, depends, lifestyle):
		self.__classtype = classtype
		self.__depends = depends
		self.__lifestyle = lifestyle
		
	@property
	def LifeStyle(self):
		return self.__lifestyle
		
	@property
	def ClassType(self):
		return self.__classtype
		
	@property
	def Depends(self):
		return self.__depends
		
class GraphSearcher(object):
	
	def match_by_class(self, graph, clstype):
		objs = []
		for k,v in graph.iteritems():
			if v.ClassType == clstype:
				objs.append((k, v))
		return objs
	
	def match_by_key(self, objs, key):
		for clstuple in objs:
			if clstuple[0] == key:
				return clstuple
		
class DefaultBuilder(object):
	
	def build_class(self,cls, dep):
		if len(dep) == 0:
			return cls()
		return cls(*dep)
	
	
class Inspector(object):
	
	def __init__(self, searcher=GraphSearcher()):
		self.__search = searcher
	
	
	def find_class_by_key_or_class(self,graph, clstype,key):
		objs  = self.__search.match_by_class(graph, clstype)
		if len(objs) > 1:
			match =  self.__search.match_by_key(objs, key)
			if match is None:
				raise Exception ("was able to find matching types but the key does not match for key " + str(key) + " and type " + str(clstype))
			return match
		if len(objs) == 1:
			return objs[0]
		raise Exception(" class type not found in object graph..this is um bad " + str(clstype) + " " + str(key))
		
		
	def initalize_cls(self,graph, key,cls):
		if cls is None:
			comp = graph[key]
			return comp.ClassType
		return cls		


class DefaultObjResolver(object):
	
	def __init__(self, inspect= Inspector()):
		self.__inspect = inspect
		
	def get_depends(self,dep,graph):
		if isinstance(dep, Config):
			dep = graph[dep.comp_key].ClassType
		deptuple = self.__inspect.find_class_by_key_or_class(graph, dep, None)
		return deptuple		

				 
class DefaultLifeStyleResolver(object):
	
	def handle_lifestyle(self, component, instances,resolvedobj,cls):
		if component.LifeStyle == "singleton":
			instances[cls] = resolvedobj
			
class DefaultResolver(object):
	
	def __init__(self, builder = DefaultBuilder(),objresolver=DefaultObjResolver() ,lifestyle = DefaultLifeStyleResolver(),inspect=Inspector() ):
		self.__builder = builder
		self.__objresolver = objresolver
		self.__lifestyle = lifestyle
		self.__inspect = inspect
		
	def walk(self,graph,key,cls,instances):
		clsout = self.__inspect.initalize_cls(graph,key,cls)
		if clsout in instances:
			return instances[cls]
		clstuple =self.__inspect.find_class_by_key_or_class(graph, clsout, key)
		deps = []
		component = clstuple[1]
		for dep in component.Depends:
			deptuple = self.__objresolver.get_depends(dep, graph)
			deps.append(self.walk(graph, deptuple[0], deptuple[1].ClassType, instances))
		resolvedobj = self.__builder.build_class(component.ClassType, deps)
		self.__lifestyle.handle_lifestyle(component, instances,resolvedobj,cls)
		return resolvedobj
	
		
	
class PinsorContainer(object):
	
	def __init__(self, resolver = DefaultResolver()):
		self.__objectgraph = {}
		self.__instances = {}
		self.__resolver = resolver
		
	def AddComponent(self,clstype, depends = [], lifestyle = LifeStyle.Singleton(), key= None):
		if key is None:
			key = clstype.__name__
		if key in self.__objectgraph:
			raise KeyError
		self.__objectgraph[key] = Component(clstype, depends, lifestyle)
			
	def Resolve(self,clstype=None,key=None):
		obj = self.__resolver.walk(self.__objectgraph, key, clstype, self.__instances)
		return obj

	@property
	def ObjectGraph(self):	
		return self.__objectgraph
		