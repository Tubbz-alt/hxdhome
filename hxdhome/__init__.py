from . import ui
from .group    import HXDHutch, HXDGroup
from .config   import ConfigReader

#Versioneer
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
