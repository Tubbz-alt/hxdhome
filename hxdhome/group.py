"""
HXDGroup definition
"""
############
# Standard #
############
import logging

###############
# Third Party #
###############
import pedl
from   pedl.utils import LocalPv, LocalEnumPv

##########
# Module #
##########

logger = logging.getLogger(__name__)



class HXDGroup(object):
    """
    Generic object grouping

    Attributes
    ----------
    children
    """
    def __init__(self, *args, name=None):
        self._design  = pedl.Designer()
        self.name     = name
        self.children = args


    @property
    def alias(self):
        """
        Cleaned name to use for programmatic use
        """
        return self.name.replace(' ','').lower()


    @property
    def devices(self):
        """
        All devices within group
        """
        devices = []
        for d in self.children:
            if isinstance(d, HXDGroup):
                devices.extend(d.devices)

            else:
                devices.append(d)

        return devices


    @property
    def subgroups(self):
        """
        All child groups
        """
        return [d for d in self.children if isinstance(d, HXDGroup)]

    @property
    def pv(self):
        """
        A EnumPV based on subgroups
        """
        if not self.subgroups:
            raise ValueError("Group has no subgroups to control") 

        #Create representative local PV
        return LocalEnumPv(self.alias, states=[g.alias
                                               for g in self.subgroups])

#    def window(self, dimensions=None):
#        if not dimensions and self.parent:
#            dimensions = self.parent.embedded_size
#
#        return GroupWindow(
#
#
#    def show(self, **kwargs):
#        self.d.setLayout(self.layout)
#        return d.show(**kwargs)
#

    def __iter__(self):
        return iter(self.devices)    
