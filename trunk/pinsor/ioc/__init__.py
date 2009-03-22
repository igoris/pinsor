"""Main component you want to import from the client side.
Should import all the necessary classes you need to configure your container"""

from pinsor.ioc.container import PinsorContainer
from pinsor.ioc.registration import Config, Instance
from pinsor.ioc.enums import LifeStyle
from pinsor.ioc.fluent import FluentService, Component
__all__ = ["PinsorContainer", "Config", \
"Instance", "LifeStyle", "FluentService", "Component"]

