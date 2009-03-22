"""contains structures the base data structures used  
for storing configuration information"""

class ComponentModel(object):
    """describes the configuration of a component"""
    def __init__(self, classtype, depends, lifestyle):
        self.classtype = classtype
        self.depends = depends
        self.lifestyle = lifestyle
        
    def to_string(self):
        """human friendly representation of component model used in debugging"""
        print str(self.classtype), str(self.depends), \
         str(self.lifestyle), str(type(self.depends))

class GraphNode(object):
    """basic object structure used to store configuration infomration"""
    def __init__(self, key, component):
        self.key = key
        self.component = component
    
