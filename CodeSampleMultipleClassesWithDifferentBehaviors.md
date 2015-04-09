# Configuration for multiple classes with different behavior #

Lets say you have classes like so:

```python


class !CsvFormat(object):

@property
def Extension(self):
return ".csv"

def getline(self,record):
line = []
for col in record:
line.append(col + ',')
rawoutput = ''.join(line)
csvoutput = rawoutput.rstrip(',')
return csvoutput

class !FileWriter(object):

def __init__(self, format):
self.__format = format

def !WriteLines(self,records, directory)
endswith = self.__format.Extension
writelist = []
for record in records:
formattedline = self.__format.getline(record)
writelist.append(formattedline)

outputpath = directory + "outputfile" + endswith
f = open(outputpath)
f.writelines(writelist)
f.close()

```

This example is a bit contrived and doesn't show the larger point of using Pinsor, however imagine you have lines spread throughout your code base like this:

```python

class !MonthlyReports(object):

def writereport(self, records):
format = !CsvFormat()
writer = !FileWriter(format)
writer.!WriteLines(records, '/mnt/share/fileserver/public/reports/')

Class !QueryResults(object):

def exportascsv(self, results):
format = !CsvFormat()
writer = !FileWriter(format)
writer.!WriteLines(results, '/home/john/queryresults')

```

Imagine there are dozens like this. Now if you're like alot of folks you end up making a class thats responsible for making these objects for you:

```python

class !MakeWriter(object):

def !GetWriter(self)
format = !CsvFormat()
writer = !FileWriter(format)
return writer
```

But lets say your boss wants you to make make half of your classes use a new CrystalReportsFormat class that another coder created. He tells you not to worry has identical properties and functions to CsvFormat, just plug it in where it matters, hands you the list of classes to change and walks out.

Now you have to make a new factory class and copy and paste the references all over your code base (potentially having to update your unit tests depending on if you were certain CsvFormat would always be there). You're careful so it takes you 20 minutes or so and tests to validate the change.

Well if you had Pinsor from the start you'd only have to change one python module that instantiates the container (and that your running code is called ServerApplication):

```python

# classes change like so
class !MonthlyReports(object):

def __init__(self, writer):
self.__writer = writer

def writereport(self, records):
self.__writer.!WriteLines(records, '/mnt/share/fileserver/public/reports/')

Class !QueryResults(object):

def __init__(self,writer):
self.__writer = writer

def exportascsv(self, results):
self.__writer.!WriteLines(results, '/home/john/queryresults')

# Pinsor code in main module

container = !PinsorContainer()
container.addcomponent(!CsvFormat)
container.addcomponent(!CrystalReportsFormat)
container.addComponent(!FileWriter,key='write.csv',depends=[ CsvFormat])
container.addcomponent(!FileWriter,key='write.crystal',depends=[ CrystalReportsFormat])
container.addcomponent(!MonthlyReports, depends=[Config('write.csv')])
container.addcomponent(!QueryResults, depends=[Config('write.crystal')])
container.addcomponent(!ServerApplication, depends=[MonthlyReports,QueryResults])

app = container.resolve(!ServerApplication)
app.start()


```

So what's going on here?  I configure every class I want to use in the application, and their dependencies. Dependency order is import as it's how Pinsor knows which argument to pass into your constructor.  For MonthlyReports and QueryResults the Dependency takes a Config class and whose argument is a key referenced from earlier, each key is pointing to a different configured instance of FileWriter.  MonthyReports will use csv formatting and QueryResults will generate a crystal report.