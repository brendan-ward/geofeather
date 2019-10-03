import json
import os
import warnings

from feather import read_dataframe
import fiona
from geopandas import GeoDataFrame

from pandas import DataFrame
from shapely.wkb import loads

# from rtree.index import Index, Property


def to_geofeather(df, path):
    """Serializes a geopandas GeoDataFrame to a feather file on disk.

    IMPORTANT: feather format does not support a non-default index; call reset_index() before using this function.

    Internally, the geometry data are converted to WKB format.

    This also creates a .crs file with CRS information for this dataset
    
    Parameters
    ----------
    df : geopandas.GeoDataFrame
    path : str
        path to feather file to write
    """

    # write the crs to an associated file
    if df.crs:
        with open("{}.crs".format(path), "w") as crsfile:
            crs = df.crs
            if isinstance(crs, str):
                crs = {"proj4": crs}
            crsfile.write(json.dumps(crs))

    df = df.copy()

    df["wkb"] = df.geometry.apply(lambda g: g.wkb)
    df = df.drop(columns=["geometry"])
    df.to_feather(path)


def from_geofeather(path):
    """Deserialize a geopandas.GeoDataFrame stored in a feather file.

    This converts the internal WKB representation back into geometry.

    If the corresponding .crs file is found, it is used to set the CRS of
    the GeoDataFrame.

    Note: no index is set on this after deserialization, that is the responsibility of the caller.
    
    Parameters
    ----------
    path : str
        path to feather file to read
    
    Returns
    -------
    geopandas.GeoDataFrame
    """

    crs = None
    crsfilename = "{}.crs".format(path)
    if os.path.exists(crsfilename):
        crs = json.loads(open(crsfilename).read())
        if "proj4" in crs:
            crs = crs["proj4"]
    else:
        warnings.warn(
            "{} coordinate reference system file is missing. No crs will be set for this GeoDataFrame.".format(
                crsfilename
            )
        )

    df = read_dataframe(path)
    df["geometry"] = df.wkb.apply(lambda wkb: loads(wkb))
    return GeoDataFrame(df.drop(columns=["wkb"]), geometry="geometry", crs=crs)
