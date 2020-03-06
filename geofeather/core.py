import json
import os
import warnings

from feather import read_dataframe
from geopandas import GeoDataFrame

from pandas import DataFrame
from shapely.wkb import loads


def _to_geofeather(df, path, crs):
    """Serializes a pandas DataFrame to a feather file on disk.
    This also creates a .crs file with CRS information for this dataset.

    Parameters
    ----------
    df : geopandas.GeoDataFrame
        Must contain a column "geometry" with WKB-encoded geometry
    path : str
        path to feather file to write
    crs : str or dict
    """

    # write the crs to an associated file
    if crs:
        with open("{}.crs".format(path), "w") as crsfile:
            # geopandas CRS is now pyproj.CRS object
            if hasattr(crs, "to_wkt"):
                crs = {"wkt": crs.to_wkt()}
            # fallbackfor older versions
            elif isinstance(crs, str):
                crs = {"proj4": crs}
            crsfile.write(json.dumps(crs))

    df.to_feather(path)


def _from_geofeather(path, columns=None):
    """Deserialize a pandas.DataFrame stored in a feather file.

    If the corresponding .crs file is found, it is used to set the CRS of
    the GeoDataFrame.

    Parameters
    ----------
    path : str
        path to feather file to read
    columns : list-like (optional, default: None)
        Subset of columns to read from the file, must include 'geometry'.  If not provided,
        all columns are read.

    Returns
    -------
    tuple of (pandas.DataFrame, dict or str)
        DataFrame will contain a "geometry" or "wkb" column with WKB-encoded geometry data.
        crs will be a dict or str depending on what was serialized.
    """
    crs = None
    crsfilename = "{}.crs".format(path)
    if os.path.exists(crsfilename):
        crs = json.loads(open(crsfilename).read())
        if "wkt" in crs:
            crs = crs["wkt"]
        elif "proj4" in crs:
            crs = crs["proj4"]
    else:
        warnings.warn(
            "{} coordinate reference system file is missing. No crs will be set for this GeoDataFrame.".format(
                crsfilename
            )
        )

    return read_dataframe(path, columns=columns), crs


def to_geofeather(df, path):
    """Serializes a geopandas GeoDataFrame to a feather file on disk.

    IMPORTANT: feather format does not support a non-default index; call reset_index() before using this function.

    Internally, the geometry data are converted to WKB format.

    This also creates a .crs file with CRS information for this dataset

    Parameters
    ----------
    df : geopandas.GeoDataFrame
        geometry must be contained in "geometry" column
    path : str
        path to feather file to write
    """

    crs = df.crs
    df = DataFrame(df.copy())

    # convert geometry field to WKB
    df.geometry = df.geometry.apply(lambda g: g.wkb)

    _to_geofeather(df, path, crs)


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

    # decode the WKB geometry back to shapely objects
    df.geometry = df.geometry.apply(lambda wkb: loads(wkb))

    return GeoDataFrame(df, geometry="geometry", crs=crs)
