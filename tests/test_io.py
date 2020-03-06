import os

from geofeather import to_geofeather, from_geofeather
from pandas.util.testing import assert_frame_equal
import pytest


def test_points_geofeather(tmpdir, points_wgs84):
    """Confirm that we can round-trip points to / from feather file"""

    filename = tmpdir / "points_wgs84.feather"
    to_geofeather(points_wgs84, filename)

    assert os.path.exists(filename)

    df = from_geofeather(filename)
    assert_frame_equal(df, points_wgs84)
    assert df.crs == points_wgs84.crs


def test_points_geofeather_proj4(tmpdir, points_albers_conus_proj4):
    """Confirm that we can round-trip points to / from feather file with a proj4 defined CRS"""

    filename = tmpdir / "points_albers_conus.feather"
    to_geofeather(points_albers_conus_proj4, filename)

    df = from_geofeather(filename)
    assert_frame_equal(df, points_albers_conus_proj4)

    # equality comparision fails for CRS object constructed from proj4, even though they are still the same
    if hasattr(df.crs, "to_proj4"):
        assert df.crs.to_proj4() == points_albers_conus_proj4.crs.to_proj4()
    else:
        assert df.crs == points_albers_conus_proj4.crs


def test_points_geofeather_wkt(tmpdir, points_albers_conus_wkt):
    """Confirm that we can round-trip points to / from feather file with a wkt defined CRS"""

    filename = tmpdir / "points_albers_conus.feather"
    to_geofeather(points_albers_conus_wkt, filename)

    df = from_geofeather(filename)
    assert_frame_equal(df, points_albers_conus_wkt)
    assert df.crs == points_albers_conus_wkt.crs


def test_missing_crs_warning(tmpdir, points_wgs84):
    """Confirm that a warning is raised if the crs file is missing"""

    filename = tmpdir / "points_wgs84.feather"
    to_geofeather(points_wgs84, filename)

    os.remove("{}.crs".format(filename))

    with pytest.warns(UserWarning) as warning:
        df = from_geofeather(filename)
        assert (
            "coordinate reference system file is missing" in warning[0].message.args[0]
        )

        assert df.crs is None


def test_lines_geofeather(tmpdir, lines_wgs84):
    """Confirm that we can round-trip lines to / from feather file"""

    filename = tmpdir / "lines_wgs84.feather"
    to_geofeather(lines_wgs84, filename)

    assert os.path.exists(filename)

    df = from_geofeather(filename)
    assert_frame_equal(df, lines_wgs84)
    assert df.crs == lines_wgs84.crs


def test_polygons_geofeather(tmpdir, polygons_wgs84):
    """Confirm that we can round-trip polygons to / from feather file"""

    filename = tmpdir / "polygons_wgs84.feather"
    to_geofeather(polygons_wgs84, filename)

    assert os.path.exists(filename)

    df = from_geofeather(filename)
    assert_frame_equal(df, polygons_wgs84)
    assert df.crs == polygons_wgs84.crs

