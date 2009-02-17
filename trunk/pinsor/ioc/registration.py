class Config(object):
	
	def __init__(self, key):
		self.__key = key
		
	@property
	def comp_key(self):
		return self.__key
		
class Instance(object):
	
	def __init__(self, arg):
		self.__arg = arg
		
	@property
	def arg(self):
		return self.__arg
		
