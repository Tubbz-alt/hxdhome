############
# Standard #
############
import logging

###############
# Third Party #
###############
import happi
from pedl.widgets import MenuButton, Circle

##########
# Module #
##########
from hxdhome import HXDGroup
from hxdhome.ui.buttons import StandIndicator, StandButton



def test_stand_button():
    group = HXDGroup(name='DG2')
    button = StandButton(group)
    assert button.stand_symbol.text == 'DG2'
    assert len(button.widgets) == 1


def test_stand_indicator():
    d1 = happi.Device(prefix='MMS:tst1')
    d2 = happi.Device(prefix='MMS:tst2')
    d3 = happi.Device(prefix='MMS:tst3')
    d4 = happi.Device(prefix='MMS:tst4')
    d5 = happi.Device(prefix='MMS:tst5')
    d6 = happi.Device(prefix='MMS:tst6')
    fk = happi.Device(prefix='CAM:tst6')
    sub  = HXDGroup(d1, d2, d3, fk,  name='sub')
    main = HXDGroup(d4, d5, d6, sub, name='main')
    button = StandIndicator(main)
    #Check button
    assert isinstance(button.widgets[0], MenuButton)
    assert str(button.widgets[0].controlPv) == str(main.pv)
    #Check columns
    assert len(button.widgets) == 8
    assert len(button.widgets[-1].widgets) == 1

    #Resize and check columns
    StandIndicator.max_col_height = 3
    button = StandIndicator(main)
    assert len(button.widgets) == 8
    assert len(button.widgets[-1].widgets) == 2
