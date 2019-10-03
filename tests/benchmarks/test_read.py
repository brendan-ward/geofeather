import geopandas as gp
import pytest

from geofeather import to_geofeather, from_geofeather, to_shp


@pytest.mark.benchmark(group="read")
def test_points_read_benchmark(tmpdir, points_wgs84, benchmark):
    """Test performance of reading feather files"""

    filename = tmpdir / "points_wgs84.feather"
    to_geofeather(points_wgs84, filename)

    benchmark(from_geofeather, filename)


@pytest.mark.benchmark(group="read")
def test_points_gp_read_file_benchmark(tmpdir, points_wgs84, benchmark):
    """Test performance of Geopandas to_file function for shapefiles"""

    filename = str(tmpdir / "points_wgs84.shp")
    points_wgs84.to_file(filename)

    benchmark(gp.read_file, filename)
