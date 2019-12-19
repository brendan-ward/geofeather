import geopandas as gp
import pytest

from geofeather.pygeos import to_geofeather, from_geofeather


@pytest.mark.benchmark(group="read-points")
def test_points_pygeos_read_benchmark(tmpdir, pg_points_wgs84, benchmark):
    """Test performance of reading feather files"""

    filename = tmpdir / "points_wgs84.feather"
    to_geofeather(pg_points_wgs84, filename)

    benchmark(from_geofeather, filename)


@pytest.mark.benchmark(group="read-lines")
def test_lines_pygeos_read_benchmark(tmpdir, pg_lines_wgs84, benchmark):
    """Test performance of reading feather files"""

    filename = tmpdir / "lines_wgs84.feather"
    to_geofeather(pg_lines_wgs84, filename)

    benchmark(from_geofeather, filename)


@pytest.mark.benchmark(group="read-polygons")
def test_polygons_pygeos_read_benchmark(tmpdir, pg_polygons_wgs84, benchmark):
    """Test performance of reading feather files"""

    filename = tmpdir / "polygons_wgs84.feather"
    to_geofeather(pg_polygons_wgs84, filename)

    benchmark(from_geofeather, filename)


@pytest.mark.benchmark(group="write-points")
def test_points_pygeos_write_benchmark(tmpdir, pg_points_wgs84, benchmark):
    """Test performance of writing geofeather files"""

    filename = tmpdir / "points_wgs84.feather"
    benchmark(to_geofeather, pg_points_wgs84, filename)


@pytest.mark.benchmark(group="write-lines")
def test_lines_pygeos_write_benchmark(tmpdir, pg_lines_wgs84, benchmark):
    """Test performance of writing geofeather files"""

    filename = tmpdir / "lines_wgs84.feather"
    benchmark(to_geofeather, pg_lines_wgs84, filename)


@pytest.mark.benchmark(group="write-polygons")
def test_polygons_pygeos_write_benchmark(tmpdir, pg_polygons_wgs84, benchmark):
    """Test performance of writing geofeather files"""

    filename = tmpdir / "polygons_wgs84.feather"
    benchmark(to_geofeather, pg_polygons_wgs84, filename)
