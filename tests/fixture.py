import pytest
from carst import SingleRaster, ConfParams

@pytest.fixture()
def test_dem():
    filepath = 'tests/data/HookerFJL_14APR02WV02DEM1_EPSG32640.tif'
    return SingleRaster(filepath)
    
@pytest.fixture()
def test_config_ft():
    filepath = 'tests/data/test_config_featuretrack.ini'
    return ConfParams(filepath)
