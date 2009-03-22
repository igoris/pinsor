"""contains exceptions used for the container and resolution issue"""
class NotFoundInObjectGraphError(Exception):
    """docstring for NotFoundInObjectGraph"""
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        """oiutputs message __str__"""
        return repr(self.message)
        