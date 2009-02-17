from enums import *
from registration import *
from components import *
from objresolution import *
 
		
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
 
						 
class DefaultLifeStyleResolver(object):
	
	def handle_lifestyle(self, lifestyle, instances,resolvedobj,cls,key):
		if lifestyle == "singleton":
			instances[key+str(cls)] = resolvedobj
			
class DefaultResolver(object):
	
	def __init__(self, builder = Builder(),objresolver=DefaultObjResolver() ,
	lifestyle = DefaultLifeStyleResolver(),inspect=Inspector() ):
		self.__builder = builder
		self.__objresolver = objresolver
		self.__lifestyle = lifestyle
		self.__inspect = inspect
		
	def recursewalk(self,graph,key,cls,instances):
		key = self.build_key(key, cls)
		clsout = self.__builder.initalize_cls(graph,key,cls)
		instance = self.find_instance(cls, instances,key)
		if instance is not None:
			return instance
		commodel =self.__inspect.find_class_by_key_or_class(graph, clsout, key)
		component = commodel.Component
		deps = self.find_deps(component, graph,instances)
		resolvedobj = self.__builder.build_class(component.ClassType, deps)
		self.__lifestyle.handle_lifestyle(component.LifeStyle, instances,resolvedobj,clsout,commodel.Key)
		return resolvedobj
	
	def build_key(self, key,cls):
		if key is None:
			key = cls.__name__
		return key
	
	def find_deps(self,component, graph,instances):
		deps =  []
		for dep in component.Depends:
			depcommodel = self.__objresolver.get_depends(dep, graph)
			deps.append(self.recursewalk(graph, depcommodel.Key, depcommodel.Component.ClassType, instances))
		return deps
			
	def find_instance(self,cls,instances, key ):
		for instkey in instances.keys():
			if instkey == key+str(cls):
				return instances[instkey]	
	
class PinsorContainer(object):
	
	def __init__(self, resolver = DefaultResolver()):
		self.__objectgraph = {}
		self.__instances = {}
		self.__resolver = resolver
		
	def AddComponent(self,clstype, depends = [],
	 lifestyle = LifeStyle.Singleton(), key= None):
		if key is None:
			key = clstype.__name__
		if key in self.__objectgraph:
			raise KeyError
		print clstype, depends, lifestyle
		self.__objectgraph[key] = ComponentModel(clstype, depends, lifestyle)
			
	def Resolve(self,clstype=None,key=None):
		obj = self.__resolver.recursewalk(self.__objectgraph, key, clstype, self.__instances)
		return obj
	
	def Register(self, *service):
		for model in service:
			componentmodel = model.GraphNode
			self.__objectgraph[componentmodel.Key] = componentmodel.Component
		

	@property
	def ObjectGraph(self):	
		return self.__objectgraph
		