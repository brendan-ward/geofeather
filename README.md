# geofeather

A faster file-based format for geometries with `geopandas`.

This project capitalizes on the very fast [`feather`](https://github.com/wesm/feather) file format to store geometry (points, lines, polygons) data for interoperability with `geopandas`.

## Why does this exist?

This project exists because reading and writing standard spatial formats (e.g., shapefile) in `geopandas` is slow. I was working with millions of geometries in multiple processing steps, and needed a fast way to read and write intermediate files.

In our benchmarks, we see about 5-6x faster file writes than writing from geopandas to shapefile via `.to_file()` on a `GeoDataFrame`.

We see about 2x faster reads compared to geopandas `read_file()` function.

## How does it work?

The `feather` format works brilliantly for standard `pandas` data frames. In order to leverage the `feather` format, we simply convert the geometry data from `shapely` objects into Well Known Binary ([WKB](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)) format, and then store that column as raw bytes.

We store the coordinate reference system using JSON format in a sidecar file `.crs`.

## Installation

`pip install geofeather`

## Usage

### Write

Given an existing `GeoDataFrame` `my_gdf`, pass this into `to_geofeather`:

```
to_geofeather(my_gdf, 'test.feather')
```

### Read

```
my_gdf = from_feather('test.feather')

```

## Indexes

Right now, indexes are not supported in `feather` files. In order to get around this, simply reset your index before calling `to_geofeather`.
