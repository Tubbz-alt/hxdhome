############
# Standard #
############

###############
# Third Party #
###############
from happi import Device

##########
# Module #
##########
from hxdhome    import HXDGroup
from hxdhome.ui import HXRAYHome, HXRAYStand, HXRAYDeviceWindow
from .conftest  import requires_edm

def test_alias():
    g = HXDGroup(name='DG2 TEST')
    assert g.alias == 'dg2_test'


def test_device_handling():
    sub_d  = Device(name='sub_device')
    main_d = Device(name='main_device')
    sub  = HXDGroup(sub_d, name='sub')
    main = HXDGroup(main_d, sub, name='main')
    assert main.children  == (main_d, sub)
    assert main.devices   == [main_d, sub_d]
    assert main.subgroups == [sub]
    assert sub.subgroups  == []


def test_pv():
    sub_1  = HXDGroup(name='sub_1')
    sub_2  = HXDGroup(name='sub_2')
    main   = HXDGroup(sub_1, sub_2, name='main')
    assert str(main.pv) == 'LOC\\\\main=e:2,sub_1,sub_2,overview'

def test_group_create_screen(simul_stand):
    screen = simul_stand.create_screen(split=False)
    assert isinstance(screen, HXRAYDeviceWindow)
    screen = simul_stand.create_screen(split=True)
    assert isinstance(screen, HXRAYStand)

def test_hutch_create_screen(simul_hutch):
    screen = simul_hutch.create_screen(split=False)
    assert isinstance(screen, HXRAYHome)

def test_device_recursion():
    bot_d  = Device(name='bot_device')
    low_d  = Device(name='low_device')
    sub_d  = Device(name='sub_device')
    main_d = Device(name='main_device')
    bot  = HXDGroup(bot_d,       name='bottom')
    low  = HXDGroup(low_d, bot,  name='low')
    sub  = HXDGroup(sub_d, low,  name='sub')
    main = HXDGroup(main_d, sub, name='main')
    assert bot_d in main.devices
    assert low_d in main.devices
    assert sub_d in main.devices


@requires_edm
def test_group_show(simul_stand):
    proc = simul_stand()
    assert not proc.poll()
    proc.terminate()
    proc = simul_stand.show(split=False)
    assert not proc.poll()
    proc.terminate()
