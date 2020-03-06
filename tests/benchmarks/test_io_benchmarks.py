import geopandas as gp
import pytest

from geofeather import to_geofeather, from_geofeather


@pytest.mark.benchmark(group="read-points")
def test_points_read_benchmark(tmpdir, points_wgs84, benchmark):
    """Test performance of reading feather files"""

    filename = tmpdir / "points_wgs84.feather"
    to_geofeather(points_wgs84, filename)

    benchmark(from_geofeather, filename)


@pytest.mark.benchmark(group="read-points")
def test_points_gp_read_file_benchmark(tmpdir, points_wgs84, benchmark):
    """Test performance of Geopandas to_file function for shapefiles"""

    filename = str(tmpdir / "points_wgs84.shp")
    points_wgs84.to_file(filename)

    benchmark(gp.read_file, filename)


@pytest.mark.benchmark(group="read-lines")
def test_lines_read_benchmark(tmpdir, lines_wgs84, benchmark):
    """Test performance of reading feather files"""

    filename = tmpdir / "lines_wgs84.feather"
    to_geofeather(lines_wgs84, filename)

    benchmark(from_geofeather, filename)


@pytest.mark.benchmark(group="read-lines")
def test_lines_gp_read_file_benchmark(tmpdir, lines_wgs84, benchmark):
    """Test performance of Geopandas to_file function for shapefiles"""

    filename = str(tmpdir / "lines_wgs84.shp")
    lines_wgs84.to_file(filename)

    benchmark(gp.read_file, filename)


@pytest.mark.benchmark(group="read-polygons")
def test_polygons_read_benchmark(tmpdir, polygons_wgs84, benchmark):
    """Test performance of reading feather files"""

    filename = tmpdir / "polygons_wgs84.feather"
    to_geofeather(polygons_wgs84, filename)

    benchmark(from_geofeather, filename)


@pytest.mark.benchmark(group="read-polygons")
def test_polygons_gp_read_file_benchmark(tmpdir, polygons_wgs84, benchmark):
    """Test performance of Geopandas to_file function for shapefiles"""

    filename = str(tmpdir / "polygons_wgs84.shp")
    polygons_wgs84.to_file(filename)

    benchmark(gp.read_file, filename)


@pytest.mark.benchmark(group="write-points")
def test_points_write_benchmark(tmpdir, points_wgs84, benchmark):
    """Test performance of writing geofeather files"""

    filename = tmpdir / "points_wgs84.feather"
    benchmark(to_geofeather, points_wgs84, filename)


@pytest.mark.benchmark(group="write-points")
def test_points_gp_to_file_benchmark(tmpdir, points_wgs84, benchmark):
    """Test performance of Geopandas to_file function for shapefiles"""

    filename = str(tmpdir / "points_wgs84.shp")
    benchmark(points_wgs84.to_file, filename)


@pytest.mark.benchmark(group="write-lines")
def test_lines_write_benchmark(tmpdir, lines_wgs84, benchmark):
    """Test performance of writing geofeather files"""

    filename = tmpdir / "lines_wgs84.feather"
    benchmark(to_geofeather, lines_wgs84, filename)


@pytest.mark.benchmark(group="write-lines")
def test_lines_gp_to_file_benchmark(tmpdir, lines_wgs84, benchmark):
    """Test performance of Geopandas to_file function for shapefiles"""

    filename = str(tmpdir / "lines_wgs84.shp")
    benchmark(lines_wgs84.to_file, filename)


@pytest.mark.benchmark(group="write-polygons")
def test_polygons_write_benchmark(tmpdir, polygons_wgs84, benchmark):
    """Test performance of writing geofeather files"""

    filename = tmpdir / "polygons_wgs84.feather"
    benchmark(to_geofeather, polygons_wgs84, filename)


@pytest.mark.benchmark(group="write-polygons")
def test_polygons_gp_to_file_benchmark(tmpdir, polygons_wgs84, benchmark):
    """Test performance of Geopandas to_file function for shapefiles"""

    filename = str(tmpdir / "polygons_wgs84.shp")
    benchmark(polygons_wgs84.to_file, filename)

