# Inversion Of Control and Dependency Injection #

## Dependencies ##
Whenever you have code reference another module or code somewhere else, you have a dependency.  This is all fine and dandy except when you want to change a bit of code but leave the rest of it the same.

Say you have a database access class, but you want to test all the code that interacts with it?  Say you have a file writer class in one format, but your customer wants you to add another file format with the same information?  In all these cases testing becomes painful, you have to start working with physical files and databases and all sorts of things can make your testing flaky and inconsistent (Python makes this less an issue but I'll get to that later).

## Dependency Injection/Inversion Of Control ##
So now you know what a Dependency is.  Dependency Injection just means you add that dependency from "outside of the class" either in a function parameter, an init constructor, or a setter on a property or attribute.  Even in languages like Python that let you easily override a function, property or constructor, this is arguably good design to make your code more readable, and more generic and reusable.

## Dependency Inversion Principle ##
Dependency Inversion refers to having your code depend on something in between your classes. Say you have a FileWriter class that depends on a CSVFormat class.  You can "invert" control of the FileWriter class to depend on a Format class which CSVFormat would inherit from.  So control is now hinging around the Format class instead of the CSVFormat class.

This is done in Java, C# and C++ with abstract classes or interfaces. Duck typing in python means this is not very necessary other than for code readability (this is an EXTREMELY heated topic for some, most of whom feel IoC is not needed in python at all). Several Python projects (PEAK, Zope, many others) have tried to enhance Python with contracts, or stronger interface support.

Most IoC containers also focus heavily on Dependency Inversion, as well as Inversion of Control. Pinsor instead focuses far more heavily on tying dependencies together for you so it does not aid very much with Dependency Inversion. But hopefully now you have some idea of why IoC containers came into existence and why users of C# and Java get so excited about them...it makes those languages more like Python able to take any class you want in a method and have your code just work.