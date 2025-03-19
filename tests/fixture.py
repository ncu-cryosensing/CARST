import pytest
from carst import SingleRaster

@pytest.fixture()
def test_dem():
    filepath = 'data/HookerFJL_14APR02WV02DEM1_EPSG32640.tif'
    return SingleRaster(filepath)
