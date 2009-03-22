""" Pinsor IoC container a Python IoC-Like Container for ease of program configuration 
Project Goals

    * Cut down lines of code for Python work.
    * Ease use of S.O.L.I.D. principles when working with Python.
    * Give Python and dynamic languages an IoC container that is based on more recent implementations. 

Features

    * Fluent Interface
    * Code-only configuration
    * Semi-automatic dependency resolution
    * No special properties or decorators needed in code
    * No need for abstract base classes to setup dependencies 
    
Examples:

---------------------------------------------------------------------------------------------
    Basic Registration:                                                                 -----
---------------------------------------------------------------------------------------------
    pinsor = PinsorContainer()
    pinsor.register(
                    Component.oftype(FakeObj)
                    )

---------------------------------------------------------------------------------------------
    Registers Dependencies
---------------------------------------------------------------------------------------------
    pinsor = PinsorContainer()
    pinsor.register(
                    Component.oftype(FakeObj),
                    Component.oftype(NeedsFakeObj).depends(FakeObj)
                    )

---------------------------------------------------------------------------------------------
    Sets component lifestyle
---------------------------------------------------------------------------------------------
    pinsor = PinsorContainer()
    pinsor.register(
                    Component.oftype(FakeObj).lifestyle(LifeStyle.transient())
                    )

---------------------------------------------------------------------------------------------
    Sets key so you can register several at once
---------------------------------------------------------------------------------------------
    pinsor = PinsorContainer()
    pinsor.register(
                    Component.oftype(FakeObj).named("fake1"),
                     Component.oftype(FakeObj).named("fake2")
                    )

---------------------------------------------------------------------------------------------
   Set up several options at once
---------------------------------------------------------------------------------------------
    pinsor = PinsorContainer()
    pinsor.register(
                    Component.oftype(FakeObj),\
                    Component.oftype(NeedsFakeObj).\
                    depends(FakeObj).\
                    lifestyle(LifeStyle.Transient())\
                    .named("needs")\
                    )
---------------------------------------------------------------------------------------------    
    """
__version__ = '0.60'

from pinsor.ioc import container, enums, registration, fluent, exceptions, components
__all__ = ["container", "enums", "registration", "fluent", "exceptions", "components"]


