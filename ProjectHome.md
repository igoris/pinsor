# UPDATE #

I know longer believe an IoC Container for Python is necessary, if you came to this page because you feel like I once did that it is I encourage you to read

http://www.lostechies.com/blogs/rssvihla/archive/2009/11/16/i-recant-my-ioc-ioc-containers-in-dynamic-languages-are-silly.aspx

## Project Goals ##

  * Cut down lines of code for Python work.
  * Ease use of [S.O.L.I.D.](SOLID.md) principles when working with Python.
  * Give Python and dynamic languages an IoC container that is based on more recent implementations.

## Features ##

  * [Fluent Interface](FluentInterface.md)
  * Code-only configuration
  * Semi-automatic dependency resolution
  * No special properties or decorators needed in code
  * No need for abstract base classes to setup dependencies

## Introduction ##

### If you know what an IoC container is ###

Pinsor aims for convention over configuration and what configuration is needed is done only in code.  It also is able to be used with minimal modification to existing source code. Extensibility will be achieved through "facilities" that tie together the core container and additional functionality.  Finally, limited AoP support will help remove the need to spread decorators over methods and match by rule, or specific reference to a classes method.

### If you do not know what an IoC(Inversion Of Control) container is ###

I'm pretty convinced Inversion Of Control (also known as Dependency Inversion Principle) is a term I've often thought was used to scare off developers new to the concept.  It's also related to a term you'll hear bandied about a lot called Dependency Injection Principle or DI, this also unnecessarily scares people.

End of the day Pinsor is designed to have you use less lines of code usually by resolving your dependencies for you (see [samples](CodeSamples.md)).  This also has the nice side effect of making your code easier to change and easier to configure.

You may use the container as much or as little as you want in your project, what matters is you use it in a way to save yourself some typing and maintenance pain, if it's not doing that for you, no one will think less of you if you remove it from your code.

#### If You still want to know what does Inversion Of Control/Dependency Injection/Dependency Inversion mean? ####

You're a glutton for punishment but I was there once myself. I know now this is actually a deceptively simple concept that's been made out to be a lot more than it is.

Martin Fowler has the most thorough explanation I've found and I can't hope to compete, but [here](http://martinfowler.com/articles/injection.html) is where I originally learned about the concept.

If you're interested I have [summary](IoCDipSummary.md) as I see it.

### Other Links Of Interest ###
  * [Project Road Map](Roadmap.md)
  * [Code Samples](CodeSamples.md)
  * [Gettting Started](GettingStarted.md)