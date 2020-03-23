# geofeather

[![Build Status](https://travis-ci.org/brendan-ward/geofeather.svg?branch=master)](https://travis-ci.org/brendan-ward/geofeather)
[![Coverage Status](https://coveralls.io/repos/github/brendan-ward/geofeather/badge.svg?branch=master)](https://coveralls.io/github/brendan-ward/geofeather?branch=master)

A faster file-based format for geometries with `geopandas`.

This project capitalizes on the very fast [`feather`](https://github.com/wesm/feather) file format to store geometry (points, lines, polygons) data for interoperability with `geopandas`.

[Introductory post](https://medium.com/@brendan_ward/introducing-geofeather-a-python-library-for-faster-geospatial-i-o-with-geopandas-341120d45ee5).

## Why does this exist?

This project exists because reading and writing standard spatial formats (e.g., shapefile) in `geopandas` is slow. I was working with millions of geometries in multiple processing steps, and needed a fast way to read and write intermediate files.

In our benchmarks, we see about 5-6x faster file writes than writing from geopandas to shapefile via `.to_file()` on a `GeoDataFrame`.

We see about 2x faster reads compared to geopandas `read_file()` function.

## How does it work?

The `feather` format works brilliantly for standard `pandas` data frames. In order to leverage the `feather` format, we simply convert the geometry data from `shapely` objects into Well Known Binary ([WKB](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)) format, and then store that column as raw bytes.

We store the coordinate reference system using JSON format in a sidecar file `.crs`.

## Installation

Available on PyPi at: https://pypi.org/project/geofeather/

`pip install geofeather`

## Usage

### Write

Given an existing `GeoDataFrame` `my_gdf`, pass this into `to_geofeather`:

```
to_geofeather(my_gdf, 'test.feather')
```

### Read

```
my_gdf = from_geofeather('test.feather')

```

### TEMPORARY

[`pygeos`](https://github.com/pygeos/pygeos) provides much faster operations of geospatial operations over arrays of geospatial data.

`geopandas` is in the process of migrating to using `pygeos` geometries as its internal data storage instead of `shapely` objects.

Until `pygeos` is fully integrated, there are shims in `geofeather` to support interoperability with pandas DataFrames containing `pygeos` geometries. If you are already using `pygeos` against data you read from `geofeather`, using the following shims will generate 3-7x speedups reading and writing data compared to `geofeather` reading into GeoDataFrames.

Internally, the feather file is identical to the one created above.

`pygeos` is required in order to use this functionality.

WARNING: this will be deprecated as soon as `pygeos` is integrated into `geopandas`.

```
from geofeather.pygeos import to_geofeather, from_geofeather

# given a DataFrame df containing pygeos geometries in 'geometry' column
# and a crs object

to_geofeather(df, 'test.feather', crs=crs)

df = from_geofeather('test.geofeather')
```

Note: no CRS information is returned when reading from geofeather into a DataFrame, in order to keep the function signature the same as above `from_geofeather`

## Indexes

Right now, indexes are not supported in `feather` files. In order to get around this, simply reset your index before calling `to_geofeather`.

## Changes

### 0.3.0

-   allow serializing to / from pandas DataFrames containing `pygeos` geometries (see notes above).
-   use new CRS object in geopandas data frames (#4)
-   dropped `to_shp`; use geopandas `to_file()` instead.

### 0.2.0

-   allow reading a subset of columns from a feather file
-   store geometry in 'geometry' column instead of 'wkb' column (simplification to avoid renaming columns)

### 0.1.0

-   Initial release

## Credits

Everything that makes this fast is due to the hard work of contributors to `pyarrow`, `geopandas`, and `shapely`.
