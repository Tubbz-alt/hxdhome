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
from hxdhome import HXDGroup


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
