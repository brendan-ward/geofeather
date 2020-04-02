import os

from geofeather.pygeos import to_geofeather, from_geofeather
from numpy import array_equal
from pandas.testing import assert_frame_equal
from pygeos import to_wkb
import pytest


GEO_CRS = "EPSG:4326"


def assert_geometry_equal(left, right):
    assert array_equal(to_wkb(left), to_wkb(right))


def test_points_geofeather(tmpdir, pg_points_wgs84):
    """Confirm that we can round-trip points to / from feather file"""

    filename = tmpdir / "points_wgs84.feather"
    to_geofeather(pg_points_wgs84, filename, crs=GEO_CRS)

    assert os.path.exists(filename)

    df = from_geofeather(filename)

    cols = df.columns.drop("geometry")
    assert_frame_equal(df[cols], pg_points_wgs84[cols])
    assert_geometry_equal(df.geometry, pg_points_wgs84.geometry)

    assert df.crs == GEO_CRS


def test_points_geofeather_no_crs(tmpdir, pg_points_wgs84):
    """Confirm that we can round-trip points to / from feather file"""

    filename = tmpdir / "points_wgs84.feather"
    to_geofeather(pg_points_wgs84, filename)

    assert os.path.exists(filename)

    with pytest.warns(UserWarning):
        df = from_geofeather(filename)

    cols = df.columns.drop("geometry")
    assert_frame_equal(df[cols], pg_points_wgs84[cols])
    assert_geometry_equal(df.geometry, pg_points_wgs84.geometry)

    assert df.crs == None


def test_lines_geofeather(tmpdir, pg_lines_wgs84):
    """Confirm that we can round-trip lines to / from feather file"""

    filename = tmpdir / "lines_wgs84.feather"
    to_geofeather(pg_lines_wgs84, filename, crs=GEO_CRS)

    assert os.path.exists(filename)

    df = from_geofeather(filename)
    cols = df.columns.drop("geometry")
    assert_frame_equal(df[cols], pg_lines_wgs84[cols])
    assert_geometry_equal(df.geometry, pg_lines_wgs84.geometry)

    assert df.crs == GEO_CRS


def test_polygons_geofeather(tmpdir, pg_polygons_wgs84):
    """Confirm that we can round-trip polygons to / from feather file"""

    filename = tmpdir / "polygons_wgs84.feather"
    to_geofeather(pg_polygons_wgs84, filename, crs="EPSG:4326")

    assert os.path.exists(filename)

    df = from_geofeather(filename)
    cols = df.columns.drop("geometry")
    assert_frame_equal(df[cols], pg_polygons_wgs84[cols])
    assert_geometry_equal(df.geometry, pg_polygons_wgs84.geometry)

    assert df.crs == GEO_CRS
