"""
Configuration control for HXDHome
"""
############
# Standard #
############
import logging

###############
# Third Party #
###############
import yaml

##########
# Module #
##########
from .group import HXDHutch, HXDGroup

logger = logging.getLogger(__name__)

class ConfigReader(object):
    """
    Class to read configuation of both the ``happi`` database

    Parameters
    ----------
    client : happi.Client
        Client to load database

    static_dir : str, optional
        Directory for static EDL files

    include : dict, optional
        Filters to include devices

    exclude : dict, optional
        Filters to exclude devices

    Attributes
    ----------
    devices : list
        List of all unsorted devices

    stands : list
        List of sorted stands

    home : :class:`.HXDHutch`
        Last loaded hutch object
    """
    def __init__(self, client, hutch=None,
                 static_dir=None, include=None,
                 exclude=None):
        #Configuration
        self.client     = client
        self.exclude    = exclude
        self.static_dir = static_dir
        #If no other information, include only hutch
        if not include and hutch:
            self.include = {'beamline' : hutch}
        else:
            self.include = include
        #Default hutch name
        self.hutch = hutch or 'hutch'
        #Parse the database
        self.reload()


    def reload(self):
        """
        Load the information from the :attr:`.client`
        """
        #Parse inclusive filters
        if not self.include:
            self.devices = self.client.all_devices
        else:
            self.devices = self.client.search(as_dict=False, **self.include)

        if not self.devices:
            raise ValueError("No devices found matching device filters")

        #Remove exclusive devices (maybe do this in happi someday)
        if self.exclude:
            self.devices = [d for d in self.devices
                            if all(getattr(d, key) != val
                            for key, val in self.exclude.items())]
        #Create stand list
        stands = dict((d.stand, list()) for d in self.devices)

        #Make sure not to add twice    
        avail_devices = dict((d.name, d) for d in self.devices)

        #Assign child devices
        for device in [d for d in self.devices if d.parent]:
            if device.name in avail_devices:
                #Find siblings
                children = [d for d in self.devices
                            if d.parent == device.parent]
                #Locate parent
                if device.parent in avail_devices.keys():
                        children.extend(avail_devices[device.parent])
                #Add to stand
                stands[device.stand].append(HXDGroup(*children,
                                                     name=device.parent))
                #Make sure devices aren't used twice
                [avail_devices.pop(d.name) for d in children]

        #Group remaining solo-devices
        for device in avail_devices.items():
            stands[device.stand].append(HXDGroup(device, name=device.name))

        #Create stands
        self.stands = [HXDGroup(*d, name=n) for n,d in stands.items()]

        #Sort stands by order on beamline
        self.stands.sort(key = lambda s : max(d.z
                                for d in s.devices))

        #Master Hutch Group
        self.home = HXDHutch(*self.stands, name=self.hutch)

        return self.home


    @classmethod
    def from_yaml(cls, client, path):
        """
        Load a configuration from a YAML file

        Parameters
        ----------
        path : str
            Path to configuration file

        Returns
        -------
        config : :class:`.ConfigReader`
            Configuration as specified in YAML file and happi
        """
        with open(path, 'r') as handle:
            cfg = yaml.load(handle.read())

        return cls(client, hutch=cfg.get('hutch'),
                   static_dir=cfg.get('static_dir'),
                   include=cfg.get('filters',{}).get('include'),
                   exclude=cfg.get('filters',{}).get('exclude'))
