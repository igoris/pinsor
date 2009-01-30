class Config(object):
	
	def __init__(self, key):
		self.__key = key
		
	@property
	def comp_key(self):
		return self.__key
		
class Param(object):
	
	def __init__(self, arg):
		self.__arg = arg
		
	@property
	def arg(self):
		return __arg
		