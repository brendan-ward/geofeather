import os

from geofeather import to_geofeather, from_geofeather, to_shp
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


def test_points_geofeather_proj4(tmpdir, points_albers_conus):
    """Confirm that we can round-trip points to / from feather file with a proj4 defined CRS"""

    filename = tmpdir / "points_albers_conus.feather"
    to_geofeather(points_albers_conus, filename)

    df = from_geofeather(filename)
    assert_frame_equal(df, points_albers_conus)
    assert df.crs == points_albers_conus.crs


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

