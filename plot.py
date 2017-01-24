from PIL import Image, ImageDraw
from PIL.ImageColor import getrgb
import random

class Plot:
    """
    Provides the ability to map, draw and color regions in a long/lat
    bounding box onto a proportionally scaled image.
    """
    @staticmethod
    def interpolate(x_1, x_2, x_3, newlength):
        """
        linearly interpolates x_2 <= x_1 <= x_3 into newlength
        x_2 and x_3 define a line segment, and x1 falls somewhere between them
        scale the width of the line segment to newlength, and return where
        x_1 falls on the scaled line.
        """
        rel_pos = x_1 / (x_3 - x_2)
        return ((x_1 - x_2) / (x_3 - x_2)) * newlength

    @staticmethod
    def proportional_height(new_width, width, height):
        """
        return a height for new_width that is
        proportional to height with respect to width
        Yields:
            int: a new height
        """
        return int((height / width) * new_width)

    @staticmethod
    def fill(region, style):
        """return the fill color for region according to the given 'style'"""
        if style == "GRAD":
            return Plot.gradient(region)
        else:
            return Plot.solid(region)

    @staticmethod
    def solid(region):
        """
        Returns a useless solid color.
        """
        return getrgb('GREEN')

    @staticmethod
    def gradient(region):
        """
        Returns a random color.
        """
        return (random.randint(1,180),random.randint(50,200),random.randint(100,255))

    def __init__(self, width, min_long, min_lat, max_long, max_lat):
        """
        Create a width x height image where height is proportional to width
        with respect to the long/lat coordinates.
        """

        self.width = width
        self.min_long = min_long
        self.min_lat = min_lat
        self.max_long = max_long
        self.max_lat = max_lat
        self.longs = (self.max_long - self.min_long)
        self.lats = (self.max_lat - self.min_lat)
        self.height = Plot.proportional_height(self.width, self.longs, self.lats)
        self.image = Image.new('RGB', (self.width, self.height), (255,255,255))




    def save(self, filename):
        """save the current image to 'filename'"""

        self.image.save(filename, 'PNG')

    def draw(self, region, style):
        """
        Draws 'region' in the given 'style' at the correct position on the
        current image
        Args:
            region (Region): a Region object with a set of coordinates
            style (str): 'GRAD' or 'SOLID' to determine the polygon's fill
        """

        def trans_long(region, new_length):
            trans_longs = [Plot.interpolate(coord, self.min_long, self.max_long, new_length) for coord in region.longs()]
            return trans_longs

        def trans_lat(region, new_length):
            trans_lats = [self.height - Plot.interpolate(coord, self.min_lat, self.max_lat, new_length) for coord in region.lats()]
            return trans_lats

        paired_coordinates = [(x, y) for x, y in zip(trans_long(region, self.width), trans_lat(region, self.height))]
        return ImageDraw.Draw(self.image).polygon(paired_coordinates, fill = Plot.fill(region, style), outline = None)
