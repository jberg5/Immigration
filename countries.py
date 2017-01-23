import csv
from pyshp import shapefile

class Country:
    """A country represented by a list of long/lat coordinates, along with a dictionary of immigration data."""
    def __init__(self,name,coords,inflow):
        self.name = name
        self.coords = coords
        self.data = {yr:ppl for yr,ppl in zip(list(range(1999,2015)),inflow)}
    def change(self,year):
        return (self.data[year-1] + self.data[year] + self.data[year+1])/3


class World:
    def __init__(self):
        self.immdat = 'ImmigrationData.csv'
        self.countries = []
        with open(self.immdat) as fin:
            csvobj = csv.reader(fin)
            for row in csvobj:
                name = row[0]
                inflow = [int(x.replace(',','')) if x != 'X' and x != ' D ' and x != 'D' and x != '-' and x != ' - ' and x != '' else 0 for x in row[1:]]
                self.countries.append(Country(name,None,inflow))


class Region:
    def __init__(self,filename):
        self.sf = shapefile.Reader(filename)
        self.shapes = self.sf.shapes()
                
