# Using Different Component LifeStyles #

When needing a class to instantiate a new copy over and over:

```python


from time import *

from pinsor.ioc import *

class CurrentTime(object):

def __init__(self):
self.time =  asctime(localtime())

def intializationtime(self):
print self.time


container = PinsorContainer()
container.addcomponent(CurrentTime, LifeStyle= LifeStyle.transient)

time1 = container.resolve(CurrentTime)
sleep(10)
time2 = container.resolve(CurrentTime)

time1.intializationtime()
Sat Jan 31 12:45:11 2009
time2.initalizationtime()
Sat Jan 31 12:45:21 2009

```

the default LifeStyle is Singleton which means that the same instance is retrieved each time resolve is called.  Singleton can still be set to make code more explicit

```python


container = PinsorContainer()
container.addcomponent(CurrentTime, LifeStyle= LifeStyle.singleton)

time1 = container.resolve(CurrentTime)
sleep(10)
time2 = container.resolve(CurrentTime)

time1.intializationtime()
Sat Jan 31 12:45:11 2009
time2.initalizationtime()
Sat Jan 31 12:45:11 2009



```