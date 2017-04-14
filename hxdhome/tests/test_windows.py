############
# Standard #
############
import os
import time
import os.path
import subprocess
from distutils.spawn import find_executable
###############
# Third Party #
###############
import pytest

##########
# Module #
##########
from hxdhome.ui.windows import HXRAYWindow, HXRAYHome, HXRAYStand

requires_edm = pytest.mark.skipif(find_executable('edm') == None,
                                  reason='EDM not found in current'\
                                         ' environment')
@requires_edm
def test_show(simul_stand):
    stnd = HXRAYStand(simul_stand)
    proc = stnd.show(block=False)
    #EDM is running
    assert not proc.poll()
    #Kill process
    proc.terminate()
    time.sleep(0.5)
    assert proc.poll() == -15


def test_save(simul_stand, temp_dir):
    #Make stand
    stnd = HXRAYStand(simul_stand)
    stnd.save(build_dir=temp_dir)
    #Check all paths
    assert all([os.path.exists(os.path.join(temp_dir,
                                            simul_stand.alias+g.alias+'.edl'))
                for g in simul_stand.subgroups])


def test_hxray_stand(simul_stand):
    stnd = HXRAYStand(simul_stand)
    #All subdisplays were made
    assert len(stnd.window.displays) == len(simul_stand.subgroups) + 1


def test_hxray_home(simul_hutch):
    hutch = HXRAYHome(simul_hutch)
    assert len(hutch.widgets[0].widgets[0].widgets) == len(simul_hutch.subgroups)
    assert len(hutch.window.displays)       == len(simul_hutch.subgroups)


def test_hxrayhome_show_displays(simul_hutch, simul_stand):
    hutch = HXRAYHome(simul_hutch)
    context = hutch._show_displays()
    #Delete files
    list(map(lambda tmp : tmp.close(), context))
    assert len(context) == len(simul_hutch.subgroups)*(len(simul_stand.subgroups)+2)


def test_hxrayhome_save_displays(simul_hutch, temp_dir):
    hutch = HXRAYHome(simul_hutch)
    hutch._save_displays(build_dir=temp_dir)
    subprocess.Popen(['ls',temp_dir])
    for stand in hutch.group.subgroups:
        assert os.path.exists(os.path.join(temp_dir,
                              simul_hutch.alias+stand.alias+'.edl'))
        assert all([os.path.exists(os.path.join(temp_dir,
                                                stand.alias+g.alias+'.edl'))
                    for g in stand.subgroups])
