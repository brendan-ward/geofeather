from geopandas import GeoDataFrame
import numpy as np
from numpy import random
from pandas import DataFrame
from pytest import fixture
from shapely.geometry import Point


@fixture
def points_wgs84():
    size = 1000
    # generate longitude -180 to 180
    x = random.sample(size) * 360 - 180
    # generate latitude -90 to 90
    y = random.sample(size) * 180 - 90

    # generate some other fields in the data frame
    i = random.randint(-32767, 32767, size=size)
    ui = random.randint(0, 65535, size=size).astype("uint64")

    df = DataFrame(data={"x": x, "y": y, "i": i, "ui": ui, "labels": i.astype("str")})
    return GeoDataFrame(
        df, geometry=df[["x", "y"]].apply(Point, axis=1), crs={"init": "EPSG:4326"}
    )


@fixture
def points_albers_conus():

    # CONUS Albers Proj4 string
    crs = "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs"

    size = 1000
    x = random.sample(size) * 100000
    y = random.sample(size) * 100000

    # generate some other fields in the data frame
    i = random.randint(-32767, 32767, size=size)
    ui = random.randint(0, 65535, size=size).astype("uint64")

    df = DataFrame(data={"x": x, "y": y, "i": i, "ui": ui, "labels": i.astype("str")})
    return GeoDataFrame(df, geometry=df[["x", "y"]].apply(Point, axis=1), crs=crs)

