"""contains classes used in configuration of components"""
class Config(object):
    """configures key value"""
    def __init__(self, key):
        self.__key = key
        
    @property
    def comp_key(self):
        """returns the component key"""
        return self.__key
        
class Instance(object):
    """stores the instance objec"""
    def __init__(self, arg):
        self.__arg = arg
        
    @property
    def arg(self):
        """retrieves the instance object"""
        return self.__arg
        
