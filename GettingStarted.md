#Learn how to get going with Pinsor

Pinsor uses parameters in the constructor to pass dependencies on. This is called "Constructor-based injection" in IoC circles it has a  counter part called "Setter-based injection" which is a lower priority for me, but I am accepting patches.

so lets get a very basic example going

```
class Job(object):
 def __init__(self,db,emailer):
     self.__db = db
     self.__emailer = emailer

 def write_and_send(self):
     records = self.__db.getrecords()
     self.__emailer.mailrecords(records)
 
class Db(object):
 def getrecords(self):
      return "xxx"
 

class Emailer(object):
 def mailrecords(self, records):
      print records 
```

now lets register these in Pinsor

```
container = PinsorContainer()
container.addcomponent(Job, depends=[Db, Emailer])
container.addcomponent(Db)
container.addcomponent(Emailer)
```

normally your code would be **each** time you need to call the job

```

db = Db()
emailer = Emailer()

job = Job(db, emailer)
```

but with the container every time you need the job you'll just have to call this (but don't get in the habit of working with the container directly, I'll get into this later)
```

job = container.resolve(Job)
```

[Continue to page 2](GettingStarted2.md)