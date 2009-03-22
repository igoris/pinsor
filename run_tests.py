import unittest
import os
import re
import sys
import inspect
import types

def loadClassesFromFolder( folderPath, packageName, baseclass ):
    classes = []
    modules = {}
    folder = os.listdir(folderPath)
    for moduleName in folder:
        modulePath = os.path.join(folderPath, moduleName)
        if not os.path.isdir(modulePath) and re.search(".py$", moduleName) and (not re.search("__init__.py", moduleName)) : 
            fullModuleName = packageName + '.' + moduleName[:-3]
            # curious: this imports the package not the module
            try:
                package = __import__(fullModuleName) 
                # it is weird indeed as __import__('packageName') does not load its modules
                for packageItem in dir(package):
                    if not modules.has_key(packageItem):
                        modules[packageItem] = True
                        moduleHandler = getattr(package, packageItem)
                        for className, classHandler in inspect.getmembers(moduleHandler, callable):
                            if inspect.isclass(classHandler) and issubclass(classHandler, baseclass):
                                classes.append(classHandler)
            except Exception, e:
                print "Warning: Exception loading module ", fullModuleName,  str(e.args)
                raise
    return classes


def makeSuite(testsFolder = 'pinsor/tests/stories', testsPackageName = 'tests', testClassSuffix='tests'):
    """Given the testsFolder parameter, loads all the .py files to search for classes
       which name contains testClassSuffix and inherit from unittest.TestCase.
       It takes these classes to buid the TestSuite and run all the tests.
    """
    testClasses = []
    testModules = {}
    testPackage = None
    suite = unittest.TestSuite()
    testClasses = loadClassesFromFolder(testsFolder, "pinsor.tests.stories", unittest.TestCase)
    for classHandler  in testClasses:
        for name, value in inspect.getmembers(classHandler, callable):
            if re.match("test", name):
                print " - Test:", name, "  (", classHandler, ")"
                suite.addTest(classHandler(name))
    return suite

if __name__ == "__main__":
    suite = makeSuite()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
