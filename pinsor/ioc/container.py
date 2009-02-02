from enums import *
from registration import *
from components import *
	
class Searcher(object):
	
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
		
class Builder(object):
	
	def build_class(self,cls, dep):
		if len(dep) == 0:
			return cls()
		return cls(*dep)
	
	def initalize_cls(self,graph, key,cls):
		if cls is None:
			comp = graph[key]
			return comp.ClassType
		return cls		
		
class Inspector(object):
	
	def __init__(self, searcher=Searcher()):
		self.__search = searcher
	
	
	def find_class_by_key_or_class(self,graph, clstype,key):
		objs  = self.__search.match_by_class(graph, clstype)
		if len(objs) > 1:
			match =  self.__search.match_by_key(objs, key)
			if match is None:
				raise Exception ("was able to find matching types but the key does not match for key " + str(key) + " and type " + str(clstype))
			return ComponentModel(match[0],match[1])
		if len(objs) == 1:
			tuple = objs[0]
			return ComponentModel(tuple[0], tuple[1])
		raise Exception(" class type not found in object graph..this is um bad " + str(clstype) + " " + str(key))
		
class DefaultObjResolver(object):
	
	def __init__(self, inspect= Inspector()):
		self.__inspect = inspect
		
	def get_depends(self,dep,graph):
		if isinstance(dep, Config):
			dep = graph[dep.comp_key].ClassType
		commodel = self.__inspect.find_class_by_key_or_class(graph, dep, None)
		return commodel		
						 
class DefaultLifeStyleResolver(object):
	
	def handle_lifestyle(self, lifestyle, instances,resolvedobj,cls,key):
		if lifestyle == "singleton":
			instances[key+str(cls)] = resolvedobj
			
class DefaultResolver(object):
	
	def __init__(self, builder = Builder(),objresolver=DefaultObjResolver() ,lifestyle = DefaultLifeStyleResolver(),inspect=Inspector() ):
		self.__builder = builder
		self.__objresolver = objresolver
		self.__lifestyle = lifestyle
		self.__inspect = inspect
		
	def recursewalk(self,graph,key,cls,instances):
		if key is None:
			key = cls.__name__
		clsout = self.__builder.initalize_cls(graph,key,cls)
		for instkey in instances.keys():
			if instkey == key+str(cls):
				return instances[instkey]
		commodel =self.__inspect.find_class_by_key_or_class(graph, clsout, key)
		deps = []
		component = commodel.Component
		for dep in component.Depends:
			depcommodel = self.__objresolver.get_depends(dep, graph)
			deps.append(self.recursewalk(graph, depcommodel.Key, depcommodel.Component.ClassType, instances))
		resolvedobj = self.__builder.build_class(component.ClassType, deps)
		self.__lifestyle.handle_lifestyle(component.LifeStyle, instances,resolvedobj,clsout,commodel.Key)
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
		print clstype, depends, lifestyle
		self.__objectgraph[key] = Component(clstype, depends, lifestyle)
			
	def Resolve(self,clstype=None,key=None):
		obj = self.__resolver.recursewalk(self.__objectgraph, key, clstype, self.__instances)
		return obj
	
	def Register(self, *service):
		for model in service:
			componentmodel = model.ComponentModel
			self.__objectgraph[componentmodel.Key] = componentmodel.Component
		

	@property
	def ObjectGraph(self):	
		return self.__objectgraph
		