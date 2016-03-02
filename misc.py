from math import radians, cos, sin, asin, sqrt
import json
from shapely.geometry import shape, Point
from shapely.wkt import loads as wkt_loads

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956  # Radius of earth in miles. Use 6371 for kms
    return c * r

def in_manhattan(lon, lat):
    # load GeoJSON file containing sectors
    with open('manhattan_polygon_osm.wkt') as f:
        for line in f:
            polygon = wkt_loads(line.strip())
    # construct point based on lat/long returned by geocoder
    point = Point(lon, lat)
    if polygon.contains(point):
        return True
    else:
        return False