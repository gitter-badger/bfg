'''
Gun factory. Returns a gun of requested type
'''
#TODO: actually it doesn't for now
from .http2 import HttpMultiGun
from ..util import AbstractFactory
from ..module_exceptions import ConfigurationError


class GunFactory(AbstractFactory):
    FACTORY_NAME = 'gun'

    def get(self, key):
        if key in self.factory_config:
            return HttpMultiGun(self.factory_config.get(key).get('target'))
        else:
            raise ConfigurationError(
                "Configuration for %s gun not found" % key)
