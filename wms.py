"""
Interactive WMS (Web Map Service)
---------------------------------

This example demonstrates the interactive pan and zoom capability
supported by an OGC web services Web Map Service (WMS) aware axes.

"""
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def main():
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.InterruptedGoodeHomolosine())
    ax.coastlines()

    url = 'https://map1c.vis.earthdata.nasa.gov/wmts-geo/wmts.cgi'
    layer = 'VIIRS_CityLights_2012'

    #ax.add_wms(wms='http://vmap0.tiles.osgeo.org/wms/vmap0',
    #           layers=['basic'])
    ax.add_wms( url,
                layers=[layer])

    plt.show()


if __name__ == '__main__':
    main()
