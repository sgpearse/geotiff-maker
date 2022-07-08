"""
Interactive WMTS (Web Map Tile Service)
---------------------------------------

This example demonstrates the interactive pan and zoom capability
supported by an OGC web services Web Map Tile Service (WMTS) aware axes.

The example WMTS layer is a single composite of data sampled over nine days
in April 2012 and thirteen days in October 2012 showing the Earth at night.
It does not vary over time.

The imagery was collected by the Suomi National Polar-orbiting Partnership
(Suomi NPP) weather satellite operated by the United States National Oceanic
and Atmospheric Administration (NOAA).

"""
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import PIL
from osgeo import gdal

# requires gdal to be installed via homebrew
# requires scipy, OWSLib

def array_to_raster(array):
    """Array > Raster
    Save a raster from a C order array.

    :param array: ndarray
    """
    dst_filename = '/a_file/name.tiff'


    # You need to get those values like you did.
    x_pixels = 16  # number of pixels in x
    y_pixels = 16  # number of pixels in y
    PIXEL_SIZE = 3  # size of the pixel...        
    x_min = 553648  
    y_max = 7784555  # x_min & y_max are like the "top left" corner.
    wkt_projection = 'a projection in wkt that you got from other file'

    driver = gdal.GetDriverByName('GTiff')

    dataset = driver.Create(
        dst_filename,
        x_pixels,
        y_pixels,
        1,
        gdal.GDT_Float32, )

    dataset.SetGeoTransform((
        x_min,    # 0
        PIXEL_SIZE,  # 1
        0,                      # 2
        y_max,    # 3
        0,                      # 4
        -PIXEL_SIZE))  

    dataset.SetProjection(wkt_projection)
    dataset.GetRasterBand(1).WriteArray(array)
    dataset.FlushCache()  # Write to disk.
    return dataset, dataset.GetRasterBand(1)  #If you need to return, remenber to return  also the dataset because the band don`t live without dataset.

#https://stackoverflow.com/questions/60282305/how-i-can-read-corner-coordinates-in-degrees
def degreesToMeters( ds, ulx, uly, lrx, lry ):
#def main():
    #wkt_srs = ds.GetProjection()
    wkt_srs = ccrs.PlateCarree()
    gt = ds.GetGeoTransform()
    xs = ds.RasterXSize
    ys = ds.RasterYSize

    ulx, uly = gdal.ApplyGeoTransform(gt, 0, 0)
    lrx, lry = gdal.ApplyGeoTransform(gt, xs, ys)

    src_srs = gdal.osr.SpatialReference()
    src_srs.ImportFromWkt(wkt_srs)

    # export GDAL_DATA=/Users/pearse/miniconda3/envs/wmts/share/gdal
    tar_srs = gdal.osr.SpatialReference()
    tar_srs.ImportFromEPSG(4326)

    # with recent versions of GDAL the axis order (x,y vs y,x) depends
    # on the projection. Force "x,y" with:
    src_srs.SetAxisMappingStrategy(gdal.osr.OAMS_TRADITIONAL_GIS_ORDER)
    tar_srs.SetAxisMappingStrategy(gdal.osr.OAMS_TRADITIONAL_GIS_ORDER)

    ct = gdal.osr.CoordinateTransformation(src_srs, tar_srs)

    # Arrays
    #arr1 = np.array([ulx,uly,0], dtype=np.float)
    #arr2 = np.array([lrx,lry,0], dtype=np.float)
    #ulx_deg, uly_deg, z1 = ct.TransformPoint(arr1)
    #lrx_deg, lry_deg, z2 = ct.TransformPoint(arr2)

    # original
    #z=0
    #ulx_deg, uly_deg = ct.TransformPoint(ulx, uly)
    #lrx_deg, lry_deg = ct.TransformPoint(lrx, lry)

    # reverse order
    #ulx_deg, uly_deg = ct.TransformPoint(uly, ulx)
    #lrx_deg, lry_deg, z2 = ct.TransformPoint(lry, lrx)

def main():
    
    import os
    print('GDAL_DATA' in os.environ)
    url = 'https://map1c.vis.earthdata.nasa.gov/wmts-geo/wmts.cgi'
    layer = 'VIIRS_CityLights_2012'
    #layer = 'GOES-West_ABI_Band2_Red_Visible_1km'

    #tiffFile = "/Users/pearse/night6.tif"
    tiffFile = "/root/colorado2.tif"

    north = 40.25
    south = 39.6
    east = -104.75
    west = -105.5

    width = 1920
    height = 1080
    #width = 3840
    #height = 2160

    #dpi = 96
    dpi = 1000
    fig = plt.figure( figsize=(width/dpi, height/dpi), tight_layout=True )
    print( fig.dpi )
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.add_wmts(url, layer)
    ax.set_extent([west, east, south, north], crs=ccrs.PlateCarree())
    ax.coastlines(resolution='50m', color='yellow')

    fig.savefig( tiffFile,
                 bbox_inches='tight',
                 pad_inches=0 )

    #platteCarree = "+proj=eqc +lat_ts=0 +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +units=m"
    platteCarree = "+proj=eqc +lat_ts=0 +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84"

    tiff    = gdal.OpenShared( tiffFile, gdal.GA_Update)
    width   = tiff.RasterXSize
    height  = tiff.RasterYSize
    print( str(width) + " " + str(height) )
   
    #north = 1689200.13960789
    '''north = 1669792.3618991
    south = 8399737.88981836
    east  = -6679169.44759641
    west  = -15584728.7110583'''
    degreesToMeters(tiff,north,west,south,east)
     
    ewPixelRes = ( east  - west  ) / width
    snPixelRes = ( south - north ) / height
    print( str(ewPixelRes) + " " + str(snPixelRes) )
    tiff.SetGeoTransform( [ west, ewPixelRes, 0, north, snPixelRes, 0 ] )
    
    '''dataset.SetGeoTransform((
        x_min,    # 0
        PIXEL_SIZE,  # 1
        0,                      # 2
        y_max,    # 3
        0,                      # 4
        -PIXEL_SIZE))  '''
    tiff.SetProjection( platteCarree )

if __name__ == '__main__':
    main()
