from geopandas import GeoDataFrame
import numpy as np
from numpy import random
from pandas import DataFrame
import pygeos as pg
from pytest import fixture
from shapely.geometry import Point, LineString, Polygon


def generate_lon_lat(size):
    """Generate arrays of longitude, latitude.

    Parameters
    ----------
    size : int
        length of arrays to generate

    Returns
    -------
    list of 2 arrays
    """

    return [random.sample(size) * 360 - 180, random.sample(size) * 180 - 90]


### Shapely geometry objects


@fixture
def points_wgs84():
    size = 1000
    x, y = generate_lon_lat(size)

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


@fixture
def lines_wgs84():
    size = 1000
    line_length = 10  # number of vertices
    # generate some fields in the data frame
    f = random.sample(size) * 360 - 180
    i = random.randint(-32767, 32767, size=size)
    ui = random.randint(0, 65535, size=size).astype("uint64")

    df = DataFrame(data={"f": f, "i": i, "ui": ui, "labels": i.astype("str")})

    # Generate random lines
    geometry = df.apply(
        lambda x: LineString(np.column_stack(generate_lon_lat(line_length))), axis=1
    )
    return GeoDataFrame(df, geometry=geometry, crs={"init": "EPSG:4326"})


@fixture
def polygons_wgs84():
    size = 1000
    x1, y1 = generate_lon_lat(size)
    x2, y2 = generate_lon_lat(size)

    # generate some fields in the data frame
    f = random.sample(size) * 360 - 180
    i = random.randint(-32767, 32767, size=size)
    ui = random.randint(0, 65535, size=size).astype("uint64")

    df = DataFrame(
        data={
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "f": f,
            "i": i,
            "ui": ui,
            "labels": i.astype("str"),
        }
    )

    # Generate random triangles
    geometry = df[["x1", "y1", "x2", "y2"]].apply(
        lambda row: Polygon(
            [[row.x1, row.y1], [row.x2, row.y1], [row.x2, row.y2], [row.x1, row.y1]]
        ),
        axis=1,
    )
    return GeoDataFrame(df, geometry=geometry, crs={"init": "EPSG:4326"})


### pygeos geometry objects


@fixture
def pg_points_wgs84():
    size = 1000
    x, y = generate_lon_lat(size)

    # generate some other fields in the data frame
    i = random.randint(-32767, 32767, size=size)
    ui = random.randint(0, 65535, size=size).astype("uint64")

    df = DataFrame(data={"x": x, "y": y, "i": i, "ui": ui, "labels": i.astype("str")})
    df["geometry"] = pg.points(np.array([x, y]).T)

    return df


@fixture
def pg_lines_wgs84():
    size = 1000
    line_length = 10  # number of vertices
    # generate some fields in the data frame
    f = random.sample(size) * 360 - 180
    i = random.randint(-32767, 32767, size=size)
    ui = random.randint(0, 65535, size=size).astype("uint64")

    df = DataFrame(data={"f": f, "i": i, "ui": ui, "labels": i.astype("str")})
    df["geometry"] = df.apply(
        lambda x: pg.linestrings(np.array(generate_lon_lat(line_length)).T), axis=1
    )

    return df


@fixture
def pg_polygons_wgs84():
    size = 1000
    x1, y1 = generate_lon_lat(size)
    x2, y2 = generate_lon_lat(size)

    # generate some fields in the data frame
    f = random.sample(size) * 360 - 180
    i = random.randint(-32767, 32767, size=size)
    ui = random.randint(0, 65535, size=size).astype("uint64")

    df = DataFrame(
        data={
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "f": f,
            "i": i,
            "ui": ui,
            "labels": i.astype("str"),
        }
    )

    # Generate random triangles
    df["geometry"] = df[["x1", "y1", "x2", "y2"]].apply(
        lambda row: pg.polygons(
            [[row.x1, row.y1], [row.x2, row.y1], [row.x2, row.y2], [row.x1, row.y1]]
        ),
        axis=1,
    )

    return df
