import pytest
from .fixture import test_config_ft

def test_config_path_storage(test_config_ft):
    assert test_config_ft.fpath == 'tests/data/test_config_featuretrack.ini'
    
def test_read_params_when_noexist(test_config_ft):
    test_config_ft.fpath = None
    with pytest.warns(UserWarning, match="No configuration file is given. No settings are read."):
        test_config_ft.ReadParam()
    
    
def test_read_params(test_config_ft):
    test_config_ft.ReadParam()
    results = {'image1': 'Demo_Data/LC08_L1TP_170002_20180401_20180416_01_T2_B8_cropped.TIF',
               'image2': 'Demo_Data/LC08_L1TP_170002_20180417_20180501_01_T2_B8_cropped.TIF',
               'image1_date': '2018-04-01',
               'image2_date': '2018-04-17'}
    assert test_config_ft.imagepair == results
    
def test_verify_params(test_config_ft):
    test_config_ft.ReadParam()
    test_config_ft.VerifyParam()
    assert type(test_config_ft.pxsettings['refwindow_x']) == int
    
def test_get_dems_negative(test_config_ft):
    test_config_ft.ReadParam()
    test_config_ft.VerifyParam()
    results = []
    assert test_config_ft.GetDEM() == results

