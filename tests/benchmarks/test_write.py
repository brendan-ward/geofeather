import geopandas as gp
import pytest

from geofeather import to_geofeather, from_geofeather, to_shp


@pytest.mark.benchmark(group="write")
def test_points_write_benchmark(tmpdir, points_wgs84, benchmark):
    """Test performance of writing geofeather files"""

    filename = tmpdir / "points_wgs84.feather"
    benchmark(to_geofeather, points_wgs84, filename)


@pytest.mark.benchmark(group="write")
def test_points_to_shp_benchmark(tmpdir, points_wgs84, benchmark):
    """Test performance of our builtin to_shp function"""

    filename = tmpdir / "points_wgs84.shp"
    benchmark(to_shp, points_wgs84, filename)


@pytest.mark.benchmark(group="write")
def test_points_gp_to_file_benchmark(tmpdir, points_wgs84, benchmark):
    """Test performance of Geopandas to_file function for shapefiles"""

    filename = str(tmpdir / "points_wgs84.shp")
    benchmark(points_wgs84.to_file, filename)
