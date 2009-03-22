"""Module used for Fluent registration this is
 the recommned approach to configuring components"""
from pinsor.ioc.components import GraphNode, ComponentModel
from pinsor.ioc.enums import LifeStyle

				
class FluentService(object):
    """Can call components functions in any order. 
    Sets wraps setup of a graph node instance"""

    def __init__(self):
        self.graphnode = None
                
    def named(self, key):
        """sets key name on graphnode"""
        self.graphnode.Key = key
        return self
    
    def depends(self, dependtuple):
        """sets dependencies on graphnode"""
        self.graphnode.component.depends = dependtuple
        return self
    
    def lifestyle(self, lifestyle):
        """sets lifes style on graphnode"""
        self.graphnode.component.lifestyle = lifestyle
        return self
        
class Component(object):
    """Starter service to enable the FluentService to start working"""

    @staticmethod           
    def oftype(clsobj):
        """factory for FluentService"""
        fluent  = FluentService()
        defaultcomponent = ComponentModel(
                                  classtype=clsobj, 
                                  depends=[], 
                                  lifestyle = LifeStyle.singleton()
                                  )
        fluent.graphnode = GraphNode(key=clsobj.__name__, 
                                     component=defaultcomponent
                                     )
        return fluent
        


