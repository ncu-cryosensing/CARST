import pytest
from .fixture import test_dem

def test_dem_path_storage(test_dem):
    assert test_dem.fpath == 'data/HookerFJL_14APR02WV02DEM1_EPSG32640.tif'

def test_set_path(test_dem):
    new_path = 'foo/bar'
    test_dem.set_path(new_path)
    assert test_dem.fpath == new_path