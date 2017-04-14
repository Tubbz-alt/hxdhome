############
# Standard #
############
import os.path
###############
# Third Party #
###############
import pedl
from happi import Device
##########
# Module #
##########
from hxdhome.ui.embedded import EmbeddedControl, EmbeddedGroup


def test_embedded_group(simul_device):
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    cntrl = EmbeddedGroup(simul_device, target_width=500)

    #Check title
    assert isinstance(cntrl.widgets[0], pedl.StackedLayout)
    assert cntrl.widgets[0].widgets[0].text == simul_device.name
    assert cntrl.widgets[0].widgets[0].w    == 500 - 2*cntrl.margin

    #Check types
    assert cntrl.embedded_types == list(map(lambda x:os.path.join(test_dir,x),
                                        ['large.edl','small.edl','tiny.edl']))

    #Check proper layouts
    #Four layouts
    assert len(cntrl.widgets) == 4
    #One large
    assert len(cntrl.widgets[1].widgets) == 1

    #2x2 grid
    assert len(cntrl.widgets[2].widgets) == 2
    assert all(len(lay.widgets) == 2 for lay in cntrl.widgets[2].widgets)

    #6x1 grid
    assert len(cntrl.widgets[3].widgets) == 6
    assert all(len(lay.widgets) == 1 for lay in cntrl.widgets[3].widgets)
