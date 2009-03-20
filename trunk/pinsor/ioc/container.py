from enums import *
from registration import *
from components import * 
from component_retriever import *
import types
			 
class DefaultResolver(object):

	def __init__(self, retrieval = ComponentModelRetrieval()):
		self.__retrieval = retrieval

	def __get_cls_from_graph(self, graph,key):
		componentmodel = graph[key]
		return componentmodel.ClassType
	
	def __find_instance(self, instances,key, cls):
		instkey = key+str(cls)
		for instance in instances:
			if instkey in instances:
				return instances[instkey]
				
	def __get_key_from_class_name(self, key, cls):
		if key is None:
			return cls.__name__
		return key

	def __build_class(self,cls ,deps):
		if len(deps) is 0:
			return cls()
		else:
			return cls(*deps)
				
	def recursewalk(self,graph,key,cls,instances):
		clsout = cls
		classkey = key
		if cls == None:
			clsout = self.__get_cls_from_graph(graph, classkey)
		else:
			classkey = self.__get_key_from_class_name(key, clsout)
		instance = self.__find_instance(instances, classkey, clsout)
		if instance is not None:
			return instance
		compmodel = self.__retrieval.get_component_model(graph, classkey, clsout)
		resolveddeps = []
		for dep in compmodel.Depends:
			if isinstance(dep, Config):
				configmodel = graph[dep.comp_key]
				resolveddeps.append(self.recursewalk(graph, dep.comp_key, configmodel.ClassType, instances))
			elif isinstance(dep, Instance):
				resolveddeps.append(dep.arg)
			else: 
				resolveddeps.append(self.recursewalk(graph,None, dep, instances))
		built =  self.__build_class(clsout, resolveddeps)
		if compmodel.LifeStyle is LifeStyle.Singleton():
			instances[classkey+str(clsout)] = built
		return built

class PinsorContainer(object):
	
	def __init__(self, resolver = DefaultResolver()):
		self.__objectgraph = {}
		self.__instances = {}
		self.__resolver = resolver
		
	def AddComponent(self,clstype, 
					depends = [],
					lifestyle = LifeStyle.Singleton(),
 					key= None):
		if key is None:
			key = clstype.__name__
		if key in self.__objectgraph:
			raise KeyError
		if type(depends) <> types.ListType:
			raise TypeError("Depends parameter has to be of type List, not " + str(type(depends)))
		self.__objectgraph[key] = ComponentModel(clstype, depends, lifestyle)
			
	def Resolve(self,clstype=None,key=None):
		obj = self.__resolver.recursewalk(self.__objectgraph, key, 
											clstype,
		 									self.__instances)
		return obj
	
	def Register(self, *services):
		for fluentservice in services:
			if fluentservice.GraphNode.Key in self.__objectgraph:
				raise KeyError
			graphnode = fluentservice.GraphNode
			self.__objectgraph[graphnode.Key] = graphnode.Component
		

	@property
	def ObjectGraph(self):	
		return self.__objectgraph
		
