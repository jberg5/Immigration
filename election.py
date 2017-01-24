import sys
import csv
import math
from country_test import Region
from plot import Plot
from pyshp import shapefile

def mercator(lat):
    """project latitude 'lat' according to Mercator"""
    lat_rad = (lat * math.pi) / 180
    projection = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    return (180 * projection) / math.pi

def main(results, boundaries, output, width, style):
    """
    Draws an image.
    This function creates an image object, constructs Region objects by reading
    in data from csv files, and draws polygons on the image based on those Regions
    Args:
        results (str): name of a csv file of election results
        boundaries (str): name of a csv file of geographic information
        output (str): name of a file to save the image
        width (int): width of the image
        style (str): either 'GRAD' or 'SOLID'
    """
    def to_point(coords):
        new_points = []
        for i in range(2, len(coords), 2):
            new_points.append((float(coords[i]), mercator(float(coords[i+1]))))
        return new_points


    sf = shapefile.Reader('ne_10m_admin_0_countries.shp')
    shapes = sf.shapes()
    regions = [Region(shapes[i].points) for i in range(len(shapes))]

    max_longs = [region.max_long() for region in regions]
    min_longs = [region.min_long() for region in regions]
    max_lats = [region.max_lat() for region in regions]
    min_lats = [region.min_lat() for region in regions]

    max_long = max(max_longs)
    max_lat = max(max_lats)
    min_long = min(min_longs)
    min_lat = min(min_lats)

    America = Plot(width, min_long, min_lat, max_long, max_lat)
    for region in regions:
        America.draw(region, style)
    America.save(output)




if __name__ == '__main__':
    results = None
    boundaries = None
    output = sys.argv[1]
    width = int(sys.argv[2])
    style = sys.argv[3]
    main(results, boundaries, output, width, style)
