import numpy as np
from pandas import DataFrame
from pandas.compat._optional import import_optional_dependency
from shapely.wkb import loads

from geofeather.core import _from_geofeather, _to_geofeather


def to_geofeather(df, path, crs=None):
    """Serializes a pandas DataFrame containing pygeos geometries to a feather file on disk.

    IMPORTANT: feather format does not support a non-default index; call reset_index() before using this function.

    Internally, the geometry data are converted to WKB format.

    This also creates a .crs file with CRS information for this dataset

    Parameters
    ----------
    df : pandas.DataFrame
    path : str
        path to feather file to write
    crs : str or dict, optional (default: None)
        GeoPandas CRS object
    """

    import_optional_dependency("pygeos", extra="pygeos is required for pygeos support.")
    from pygeos import to_wkb

    df = DataFrame(df.copy())
    df["geometry"] = to_wkb(df.geometry)

    _to_geofeather(df, path, crs=crs)


def from_geofeather(path, columns=None):
    """Deserialize a geopandas.GeoDataFrame stored in a feather file.

    This converts the internal WKB representation back into geometry.

    If the corresponding .crs file is found, it is used to set the CRS of
    the GeoDataFrame.

    Note: no index is set on this after deserialization, that is the responsibility of the caller.

    Parameters
    ----------
    path : str
        path to feather file to read
    columns : list-like (optional, default: None)
        Subset of columns to read from the file, must include 'geometry'.  If not provided,
        all columns are read.

    Returns
    -------
    geopandas.GeoDataFrame
    """

    import_optional_dependency("pygeos", extra="pygeos is required for pygeos support.")
    from pygeos import from_wkb

    if columns is not None and "geometry" not in columns:
        raise ValueError(
            "'geometry' must be included in list of columns to read from feather file"
        )

    # shim to support files created with geofeather 0.1.0
    if columns is not None and "wkb" not in columns:
        columns.append("wkb")

    df, crs = _from_geofeather(path, columns=columns)

    # shim to support files created with geofeather 0.1.0
    df = df.rename(columns={"wkb": "geometry"})

    df["geometry"] = from_wkb(df.geometry)

    # NOTE: no CRS information is returned at this time
    return df
