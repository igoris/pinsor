class ComponentModel(object):
    
    def __init__(self, classtype, depends, lifestyle):
        self.ClassType = classtype
        self.Depends = depends
        self.LifeStyle = lifestyle
    def to_string(self):
        print str(self.ClassType), str(self.Depends), str(self.LifeStyle), str(type(self.Depends))

class GraphNode(object):

    def __init__(self, key, component):
        self.Key = key
        self.Component = component
    
