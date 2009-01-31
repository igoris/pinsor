import unittest

def IsAnInstanceOf(instance, Class):
	status = isinstance(instance, Class)
	if status is False:
		print "expected type was " + str(Class.__class__)  +" instead the type is " + str(instance.__class__)
		raise AssertionError
		
def DictContainsValue(dict, obj):
	for k,v in dict.iteritems():
		if v == obj:
			return True
	print "does not contain " + str(obj)
	raise AssertionError
	
def ListContainsValue(list, obj):
	for o in list:
		if o == obj:
			return True
	print "does not contain " + str(obj)
	raise AssertionError