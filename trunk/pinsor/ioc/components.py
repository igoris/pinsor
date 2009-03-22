"""contains structures the base data structures used  
for storing configuration information"""

from pinsor.ioc.exceptions import AttemptToAddDuplicateComponentModelToVisitedSet

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
        
class ComponentSet(object):
    """unique collection class with checks for duplicate configuration"""
    
    def __init__(self):
        self.__comlist = []
    
        
    def __check_for_existing(self , commodel):
        """iterates through the list and returns true or false if component is in list or not"""
        for com in self.__comlist:
            dupclass = com.classtype is commodel.classtype
            dupdep = com.depends == commodel.depends
            duplife = com.lifestyle is commodel.lifestyle
            if dupclass and dupdep and duplife:
                return True
        return False
        
    def add(self, commodel):
        """adds non duplicate items to the list"""
        if self.__check_for_existing(commodel):
            raise AttemptToAddDuplicateComponentModelToVisitedSet(
            "already found comp with " +str(commodel.classtype) + \
            " and lifestyle " + str(commodel.lifestyle)
            )
        self.__comlist.append(commodel)

    def has_comp(self, commodel):
        """publc interface for checking for existing component"""
        return self.__check_for_existing(commodel)