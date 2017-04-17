############
# Standard #
############
import copy
import os.path
import shutil
from distutils.spawn import find_executable
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
from hxdhome    import HutchGroup, HXDGroup

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
             Device(name='a',prefix='MMS:a',embedded_screen=os.path.join(test_dir,'tiny.edl')),
             Device(name='b',prefix='MMS:b',embedded_screen=os.path.join(test_dir,'tiny.edl')),
             Device(name='c',prefix='MMS:c',embedded_screen=os.path.join(test_dir,'tiny.edl')),
             Device(name='d',prefix='MMS:d',embedded_screen=os.path.join(test_dir,'tiny.edl')),
             Device(name='e',prefix='MMS:e',embedded_screen=os.path.join(test_dir,'tiny.edl')),
             Device(name='f',prefix='MMS:f',embedded_screen=os.path.join(test_dir,'tiny.edl')),
             Device(name='g',prefix='MMS:g',embedded_screen=os.path.join(test_dir,'small.edl')),
             Device(name='h',prefix='MMS:h',embedded_screen=os.path.join(test_dir,'small.edl')),
             Device(name='i',prefix='MMS:i',embedded_screen=os.path.join(test_dir,'small.edl')),
             Device(name='j',prefix='MMS:j',embedded_screen=os.path.join(test_dir,'small.edl')),
             Device(name='k',prefix='MMS:k',embedded_screen=os.path.join(test_dir,'large.edl')),
             name='Device Group')

    return group


@pytest.fixture(scope='module')
def simul_stand(simul_device):
    #Create subdevices
    dev_1 = copy.copy(simul_device)
    dev_1.name = 'Device One'
    dev_2 = copy.copy(simul_device)
    dev_2.name = 'Device Two'
    dev_3 = copy.copy(simul_device)
    dev_3.name = 'Device Three'
    return HXDGroup(dev_1,dev_2,dev_3,name='Stand Group')


@pytest.fixture(scope='module')
def simul_hutch(simul_stand):
    stand_1 = copy.copy(simul_stand)
    stand_1.name = 'DIA'
    stand_2 = copy.copy(simul_stand)
    stand_2.name = 'DG1'
    stand_3 = copy.copy(simul_stand)
    stand_3.name = 'DG2'
    stand_4 = copy.copy(simul_stand)
    stand_4.name = 'SC1'
    stand_5 = copy.copy(simul_stand)
    stand_5.name = 'DG3'
    stand_6 = copy.copy(simul_stand)
    stand_6.name = 'SC2'
    stand_7 = copy.copy(simul_stand)
    stand_7.name = 'SC3'
    stand_8 = copy.copy(simul_stand)
    stand_8.name = 'DG4'
    return HutchGroup(stand_1, stand_2, stand_3, stand_4,
                    stand_5, stand_6, stand_7, stand_8,
                    name='TST')


class ExampleHutchWindow(HXRAYHome):
    def __init__(self):
        super(ExampleHutchWindow, self).__init__(simul_hutch(simul_stand(simul_device())))
