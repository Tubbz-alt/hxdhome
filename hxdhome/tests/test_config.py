############
# Standard #
############
import os.path
###############
# Third Party #
###############


##########
# Module #
##########
from hxdhome import ConfigReader


def test_cfg_loading(happiDB):
    cfg = ConfigReader(happiDB, hutch='TST')
    #Check devices were loaded
    assert len(cfg.devices) == 265

    #Check that HXDHutch was property initialized
    assert [stand.name for stand in cfg.home.subgroups] == [
                                                'DIA', 'DG1', 'DG2', 'SC1',
                                                'DG3', 'SC2', 'SC3', 'DG4']
    assert len(cfg.home.devices) == 265

    #Test on the fly grouping
    assert 'Child' in [d.name for d in cfg.home.dg4.devices]

    #Try inclusions / exclusions
    cfg = ConfigReader(happiDB, hutch='TST',
                       include={'system' : 'vacuum'},
                       exclude={'stand'  : 'DIA'})
    assert len(cfg.devices) == 126
    assert 'DIA' not in [stand.name for stand in cfg.stands]

def test_yaml_load(happiDB):
    test_dir = os.path.dirname(os.path.abspath(__file__))
    cfg = ConfigReader.from_yaml(happiDB, os.path.join(test_dir,
                                                       'test.yaml'))
    assert len(cfg.devices) == 126
    assert [stand.name for stand in cfg.home.subgroups] == ['DG1', 'DG2', 'SC1',
                                                            'DG3', 'SC2', 'SC3',
                                                            'DG4']
