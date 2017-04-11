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

    Instead of passing around lists of ``happi`` objects, information is
    combined together into sensible groups. Grouped objects don't need to be
    the same type, instead the overall strategy is to sort objects by the stand
    they belong to, and then, by using :attr:`.subgroups`, smaller device
    groups.

    Parameters
    -----------
    args : :class:`.happi.Device` or :class:`.HXDGroup`
        Series of similar objects

    name : str
        Name for the grouping

    Attributes
    ----------
    children : tuple
        Stored devices and subgroups
    """
    def __init__(self, *args, name=None):
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
        All devices within the group, created by flattening :attr:`.subgroups`
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
