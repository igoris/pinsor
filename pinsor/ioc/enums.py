"""seperate module to store enumerations. currently only LifeStyle in there"""
class LifeStyle(object):
    """lists valid options for component lifestyle"""
    
    @staticmethod
    def transient():
        """means component that is reinstantiated each time"""
        return "transient"
    
    @staticmethod
    def singleton():
        """means component that is instantiated only once 
        and repeatedly references the same instance"""
        return "singleton"