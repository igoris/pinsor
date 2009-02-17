class ComponentModel(object):
	
	def __init__(self, classtype, depends, lifestyle):
		self.ClassType = classtype
		self.Depends = depends
		self.LifeStyle = lifestyle
	

class GraphNode(object):

	def __init__(self, key, component):
		self.Key = key
		self.Component = component
	