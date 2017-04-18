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
from .ui import HXRAYHome, HXRAYDeviceWindow, HXRAYStand

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

        #Add subgroups as attributes
        for group in self.subgroups:
            setattr(self, group.alias, group)

    @property
    def alias(self):
        """
        Cleaned name to use for programmatic use
        """
        return self.name.replace(' ','_').lower()


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

        states = [g.alias for g in self.subgroups] + ['overview']
        #Create representative local PV
        return LocalEnumPv(self.alias, states=states, value='overview')


    def create_screen(self, split=True):
        """
        Create an EDM screen for the group

        Parameters
        ----------
        split : bool, optional
            Choice to show subgroups on separate screens. If there are no
            subgroups this is irrelevant

        Returns
        --------
        screen : :class:`.HXRAYStand` or :class:`.HXRAYDeviceWindow`
            Either a group of embedded windows split by group or a single page
            with all the child devices
        """
        if not split or not self.subgroups:
            return HXRAYDeviceWindow(self)
        else:
            return HXRAYStand(self)



    def show(self, split=True, block=False):
        """
        Show the EDM screen for the group

        Parameters
        ----------
        split : bool, optional
            Choice to show subgroups on separate screens. If there are no
            subgroups this is irrelevant

        block : bool, optional
            Block the main thread while the EDM screen is open

        Returns
        -------
        proc : subprocess.Popen
            Process that contains EDM process
        """
        return self.create_screen(split=split).show(block=block)


    def __call__(self):
        """
        Launch the screen when called
        """
        return self.show(split=True, block=False)


    def __repr__(self):
        return 'HXDGroup "{:}", {:} devices'.format(self.name, len(self.devices))


    def __copy__(self):
        """
        Convienence for copying group
        """
        return HXDGroup(*self.children, name=self.name)

class HXDHutch(HXDGroup):
    """
    Reimplementation of HXDGroup for entire hutch
    """
    def create_screen(self, **kwargs):
        """
        Create an EDM screen for the hutch

        Returns
        --------
        screen : :class:`.HXRAYHome`
            Home screen for hutch
        """
        return HXRAYHome(self)
