import fiona
from geopandas.io.file import infer_schema
import numpy as np
from pandas import DataFrame
from shapely.geometry import mapping


def to_shp(df, path):
    """Internal method for converting to shapefiles, when GeoPandas to_file was slow.
    
    NOTE: the GeoPandas to_file method seems to have recently improved, so this may no longer be needed!
    
    """

    # Convert data types to those supported by shapefile
    df = df.copy()
    for c in [c for c, t in df.dtypes.items() if t == "uint64"]:
        df[c] = df[c].astype("float64")

    geom_col = df._geometry_column_name
    prop_cols = [c for c in df.columns if c != geom_col]
    # Drop any records with missing geometries
    df = df.loc[~df[geom_col].isnull()].copy()
    geometry = df[geom_col].apply(mapping)
    # fill missing data with None and convert to dict
    props = df.drop(columns=[df._geometry_column_name])
    props.replace({c: {np.nan: None} for c in prop_cols}, inplace=True)
    props = props.apply(lambda row: row.to_dict(), axis=1)
    # Convert features to JSON
    features = DataFrame({"geometry": geometry, "properties": props})
    features["type"] = "Feature"
    features = features.apply(lambda row: row.to_dict(), axis=1)
    schema = infer_schema(df)
    with fiona.Env():
        with fiona.open(
            path, "w", driver="ESRI Shapefile", crs=df.crs, schema=schema
        ) as writer:
            writer.writerecords(features)

