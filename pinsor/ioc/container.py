"""where most of the magic and pain happens, some 
serious refactoring needs to be implemented here"""
from pinsor.ioc.enums import LifeStyle
from pinsor.ioc.registration import Config, Instance
from pinsor.ioc.components import ComponentModel
from pinsor.ioc.component_retriever import ComponentModelRetrieval
import types
             
class DefaultResolver(object):
    """Handles Responsibility for finding class types, instances,
     and keys, also has recurser REFACTOR THIS"""
    def __init__(self, retrieval = ComponentModelRetrieval()):
        self.__retrieval = retrieval

    def __get_cls_from_graph(self, graph, key):
        """wondering if there is a point here. seems silly REFACTOR"""
        componentmodel = graph[key]
        return componentmodel.classtype
    
    def __find_instance(self, instances, key, cls):
        """looks over the instance array by key+cls combo"""
        instkey = key+str(cls)
        if instkey in instances:
            return instances[instkey]
                
    def __get_key_from_class_name(self, key, cls):
        """retrieves key name from a class. this feels bad REFACTOR"""
        if key is None:
            return cls.__name__
        return key

    def __build_class(self, cls, deps):
        """calls the constructor dynamically"""
        if len(deps) is 0:
            return cls()
        else:
            return cls(*deps)
                
    def recursewalk(self, graph, key, cls, instances):
        """method responsible for walking the tree, 
        this is doing too much REFACTOR"""
        clsout = cls
        classkey = key
        if cls == None:
            clsout = self.__get_cls_from_graph(graph, classkey)
        else:
            classkey = self.__get_key_from_class_name(key, clsout)
        instance = self.__find_instance(instances, classkey, clsout)
        if instance is not None:
            return instance
        compmodel = self.__retrieval.get_component_model(
                                                        graph, classkey, clsout
                                                        )
        resolveddeps = []
        for dep in compmodel.depends:
            if isinstance(dep, Config):
                configmodel = graph[dep.comp_key]
                resolveddeps.append(
                                    self.recursewalk(
                                    graph, dep.comp_key, 
                                    configmodel.classtype, instances
                                    )
                                    )
            elif isinstance(dep, Instance):
                resolveddeps.append(dep.arg)
            else: 
                resolveddeps.append(
                                    self.recursewalk(
                                    graph, None, dep, instances
                                    )
                                    )
        built =  self.__build_class(clsout, resolveddeps)
        if compmodel.lifestyle is LifeStyle.singleton():
            instances[classkey+str(clsout)] = built
        return built

class PinsorContainer(object):
    """public interface to use Pinsor Adds Components and Resolves them"""
    def __init__(self, resolver = DefaultResolver()):
        self.__objectgraph = {}
        self.__instances = {}
        self.__resolver = resolver
        
    def addcomponent(self, clstype, 
                    depends = [],
                    lifestyle = LifeStyle.singleton(),
                    key= None):
        """alternative way to register components. this is not the preferred
         way but can be easier to use for those new to IoC containers"""
        if key is None:
            key = clstype.__name__
        if key in self.__objectgraph:
            raise KeyError
        if type(depends) is not types.ListType:
            raise TypeError(
            "Depends parameter has to be of type List, not "\
             + str(type(depends))
            )
        self.__objectgraph[key] = ComponentModel(clstype, depends, lifestyle)
            
    def resolve(self, clstype=None, key=None):
        """standard client way of accessing Components"""
        obj = self.__resolver.recursewalk(self.__objectgraph, key, 
                                            clstype,
                                            self.__instances)
        return obj
    
    def register(self, *services):
        """client interface to use the FluentService"""
        for fluentservice in services:
            if fluentservice.graphnode.key in self.__objectgraph:
                raise KeyError
            graphnode = fluentservice.graphnode
            self.__objectgraph[graphnode.key] = graphnode.component
        

    @property
    def objectgraph(self):
        """dictionary of all configuration information should ideally 
        not be worked with directly, here for testing and extensibility"""  
        return self.__objectgraph
        
