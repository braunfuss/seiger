import os
import gdal
import matplotlib
import numpy as num
from mpl_toolkits.basemap import Basemap


def read_usgs_vs30():
    filename = "global_vs30.tif"
    dataset = gdal.Open(filename)
    band = dataset.GetRasterBand(1)

    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    transform = dataset.GetGeoTransform()

    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = -transform[5]

    data = band.ReadAsArray(0, 0, cols, rows)
    return data, xOrigin, yOrigin, pixelWidth, pixelHeight


def extract_rectangle(lonmin, lonmax, latmin, latmax):
    data, xOrigin, yOrigin, pixelWidth, pixelHeight = read_usgs_vs30()
    p1 = (lonmin, lonmax)
    p2 = (latmin, latmax)
    col1 = int((p1[0] - xOrigin) / pixelWidth)
    row1 = int((yOrigin - p1[1]) / pixelHeight)
    col2 = int((p2[0] - xOrigin) / pixelWidth)
    row2 = int((yOrigin - p2[1]) / pixelHeight)
    values = []
    cols = num.arange(col1, col2)
    rows = num.arange(row1, row2)
    for r in rows:
        for c in cols:
            values.append(data[r][c])
    values = np.asarray(values)
    values = values.reshape(len(rows), len(cols))

    return values

p1 = (8.225, 54.931)
p2 = (10.425, 50.131)
