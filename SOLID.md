#Acronym of principles coined by Bob Martin and called SOLID by Micheal Feathers see [here ](http://www.lostechies.com/blogs/chad_myers/archive/2008/03/07/pablo-s-topic-of-the-month-march-solid-principles.aspx) for more detail

# S.ingle Responsibility Principle #

Each Class and Method should only have one reason for change.  Reason for change is dependent on context.

From the class point of view an EmployeeDatabaseAccess would only have responsibility for storage of data, but it would be harmful to add notification of management for employees having more than 40 hours in a week to this class.  This ends up with two reasons to change a class, making not only testing harder, but meaning more unintended side effects over time.

From a method or function consider things at a lower level.  Maybe set a limit of 2-3 if statements per method(early code of Pinsor violates this principle).

From a Python perspective this is still absolutely critical, arguably more so as you can so easily cause unintended behavior if not paying attention.

# O.pen/Closed Principle #

Open for Extension/Closed for modification.

Short summary rule is depend on base classes and not on specialty ones.  Example:  Your FileWriter should depend on Format not the specialized classes CsvFormat or SpaceDelimitedFormat.

While critically necessary for flexible software in static languages like C# and Java, I'm still undecided about it's value in Python.  Python 2.6 and 3.0 did add support for Abstract Base Classes which would indicate there is some value in explicitly declaring a base class with no behavior, but with the type system in Python this can be accomplished with some discipline (which the next principle addresses well)

# L.iskov Substitution Principle #

Let q(x) be a property provable about objects x of type T. Then q(y) should be true for objects y of type S where S is a subtype of T

Shorter version of the above would be once a class is specialized methods that depend on it do not depend on the specialized properties or methods.

A writeFile method should operate the same with no code checking for specific type if you give it a CsvFormat or a SpaceDelimitedFormat.  This is absolutely paramount to flexible design in any language as well as Python.  A method that does type checking has a dependency on that type directly, the more type checking the greater potential for unnecessary dependencies.

# I.nterface Segration Principle #

Clients should not depend on an interface that they do not use.

Short concept here is interfaces should be kept small.

In Python this ends up happening for free with duck typing.However, abstract base classes and if they become popular or not will change how important this principle will be.

# D.ependency Inversion Principle #

Depend on the most abstract thing you can get away with. Again in Python you get this for free with Duck Typing.