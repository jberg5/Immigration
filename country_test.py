from pyshp import shapefile

class Region:
    def __init__(self,coords):
        self.coords = coords

    def lats(self):
        "Return a list of the latitudes of all the coordinates in the region"
        latitudes = [coord[1] for coord in self.coords]
        return latitudes

    def longs(self):
        "Return a list of the longitudes of all the coordinates in the region"

        longitudes = [coord[0] for coord in self.coords]
        return longitudes

    def min_lat(self):
        "Return the minimum latitude of the region"

        return min(self.lats())

    def min_long(self):
        "Return the minimum longitude of the region"

        return min(self.longs())

    def max_lat(self):
        "Return the maximum latitude of the region"

        return max(self.lats())

    def max_long(self):
        "Return the maximum longitude of the region"

        return max(self.longs())

class World:
    def __init__(self,filename):
        sf = shapefile.Reader(filename)
        shapes = sf.shapes
        self.regions = [Region(shapes[i].points) for i in range(len(shapes))]
