############
# Standard #
############
import copy
import os.path
import shutil
from distutils.spawn import find_executable
from functools import partial
###############
# Third Party #
###############
import pytest
import happi.tests
from happi import Device

##########
# Module #
##########
from hxdhome.ui import HXRAYHome
from hxdhome    import ConfigReader, HXDHutch, HXDGroup

@pytest.fixture(scope='function')
def temp_dir():
    #Make temporary directory by hand until Python 3.x
    tmp_dir = 'testhome'
    os.makedirs(tmp_dir)
    yield os.path.abspath(tmp_dir)
    #Cleanup
    shutil.rmtree(tmp_dir)

requires_edm = pytest.mark.skipif(find_executable('edm') == None,
                                  reason='EDM not found in current'\
                                         ' environment')

@pytest.fixture(scope='module')
def simul_device():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    group = HXDGroup(
             Device(name='a',prefix='MMS:a',embedded_screen=os.path.join(test_dir,'tiny.edl'),
                    beamline='TST', system='vacuum'),
             Device(name='b',prefix='MMS:b',embedded_screen=os.path.join(test_dir,'tiny.edl'),
                    beamline='TST',system='vacuum'),
             Device(name='c',prefix='MMS:c',embedded_screen=os.path.join(test_dir,'tiny.edl'),
                    beamline='TST', system='vacuum'),
             Device(name='d',prefix='MMS:d',embedded_screen=os.path.join(test_dir,'tiny.edl'),
                    beamline='TST', system='vacuum'),
             Device(name='e',prefix='MMS:e',embedded_screen=os.path.join(test_dir,'tiny.edl'),
                    beamline='TST', system='vacuum'),
             Device(name='f',prefix='MMS:f',embedded_screen=os.path.join(test_dir,'tiny.edl'),
                    beamline='TST', system='vacuum'),
             Device(name='g',prefix='MMS:g',embedded_screen=os.path.join(test_dir,'small.edl'),
                    beamline='TST', system='timing'),
             Device(name='h',prefix='MMS:h',embedded_screen=os.path.join(test_dir,'small.edl'),
                    beamline='TST', system='timing'),
             Device(name='i',prefix='MMS:i',embedded_screen=os.path.join(test_dir,'small.edl'),
                    beamline='TST', system='timing'),
             Device(name='j',prefix='MMS:j',embedded_screen=os.path.join(test_dir,'small.edl'),
                    beamline='TST', system='timing'),
             Device(name='k',prefix='MMS:k',embedded_screen=os.path.join(test_dir,'large.edl'),
                    beamline='TST', system='diagnostics'),
             name='Device Group')

    return group


@pytest.fixture(scope='module')
def simul_stand(simul_device):
    #Create subdevices
    dev_1 = copy.deepcopy(simul_device)
    dev_1.name = 'Device One'
    dev_2 = copy.deepcopy(simul_device)
    dev_2.name = 'Device Two'
    dev_3 = copy.deepcopy(simul_device)
    dev_3.name = 'Device Three'
    return HXDGroup(dev_1,dev_2,dev_3,name='Stand Group')


@pytest.fixture(scope='module')
def simul_hutch(simul_stand):

    stand_tuples = [('DIA', 0),  ('DG1', 10), ('DG2', 15), ('SC1', 25),
                    ('DG3', 30), ('SC2', 35), ('SC3', 40), ('DG4', 50)]

    def create_stand(name, position):
        stand = copy.deepcopy(simul_stand)
        stand.name = name
        for group in stand.subgroups:
            group.name = ' '.join([name, group.name])
            for d in group.devices:
                d.z = position
                d.name   = ' '.join([stand.name,group.name.split()[2],d.name])
                d.prefix = ':'.join([stand.name,
                                     group.name.split()[2],
                                     d.prefix])
                d.stand  = name
                d.parent = group.name

        return stand

    stands = [create_stand(n, p) for n,p in stand_tuples]
    return HXDHutch(*stands, name='TST')

@pytest.fixture(scope='module')
def happiDB(simul_hutch):
    test_dir = os.path.dirname(os.path.abspath(__file__))
    client   = happi.tests.MockClient()
    #Fill database
    for device in simul_hutch.devices:
        client.add_device(device)
    #Add a parent device to be added to group
    client.add_device(Device(name='Child', prefix='Tst:MMS',
                             parent='DG4 Device Three', stand='DG4', beamline='TST',
                             embedded_screen=os.path.join(test_dir,'small.edl')))
    return client


##############
# DEMO TOOLS #
##############

def load_example_hutch():
    stand = simul_stand(simul_device())
    return simul_hutch(stand)

class ExampleHutchWindow(HXRAYHome):
    def __init__(self):
        super(ExampleHutchWindow, self).__init__(load_example_hutch())


class ExampleConfig(ConfigReader):
    def __init__(self, **kwargs):
        super(ExampleConfig,self).__init__(happiDB(load_example_hutch()),
                                           **kwargs)

ExampleDB = partial(happiDB,load_example_hutch())

