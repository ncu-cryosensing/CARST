import pytest
from .fixture import test_dem

def test_dem_path_storage(test_dem):
    assert test_dem.fpath == 'tests/data/HookerFJL_14APR02WV02DEM1_EPSG32640.tif'

def test_set_path(test_dem):
    new_path = 'foo/bar'
    test_dem.set_path(new_path)
    assert test_dem.fpath == new_path
    
def test_get_x_res(test_dem):
    assert test_dem.get_x_res() == 3.0
    
def test_get_y_res(test_dem):
    assert test_dem.get_y_res() == -3.0
    
def test_get_x_size(test_dem):
    assert test_dem.get_x_size() == 2694
    
def test_get_y_size(test_dem):
    assert test_dem.get_y_size() == 1295
    
def test_get_nodata(test_dem):
    assert test_dem.get_nodata() == -9999.0
    
def test_get_epsg(test_dem):
    assert test_dem.get_epsg() == 32640
    

