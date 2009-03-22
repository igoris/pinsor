"""Module used for Fluent registration this is the recommned approach"""
from pinsor.ioc.components import GraphNode, ComponentModel
from pinsor.ioc.enums import LifeStyle

				
class FluentService(object):
    """Can call components functions in any order. 
    Sets wraps setup of a graph node instance"""

    def __init__(self):
        self.GraphNode = None
                
    def named(self, key):
        """sets key name on graphnode"""
        self.GraphNode.Key = key
        return self
    
    def depends(self, dependtuple):
        """sets dependencies on graphnode"""
        self.GraphNode.Component.Depends = dependtuple
        return self
    
    def lifestyle(self, lifestyle):
        """sets lifes style on graphnode"""
        self.GraphNode.Component.LifeStyle = lifestyle
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
                                  lifestyle = LifeStyle.Singleton()
                                  )
        fluent.GraphNode = GraphNode(key=clsobj.__name__, 
                                     component=defaultcomponent
                                     )
        return fluent
        


