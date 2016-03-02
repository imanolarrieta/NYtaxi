# Test of misc function
from misc import *

def test_in_manhattan():
    # positive test points using google maps
    points_manhattan = [(40.769898, -73.974733),
                        (40.738690, -74.000826),
                        (40.802132, -73.943148),
                        (40.774578, -73.985720)]

    # negative test point using google maps
    points_not_manhattan = [(40.822400, -73.977480),
                            (40.719872, -74.041974),
                            (40.688639, -73.945157),
                            (41.053139, -74.317318),
                            (40.806204, -76.588742)]

    for (lat,lon) in points_manhattan:
        in_location = in_manhattan(lon, lat)
        print in_location
        assert in_location == True

    for (lat,lon) in points_not_manhattan:
        in_location = in_manhattan(lon, lat)
        print in_location
        assert in_location == False

def test_haversine():
    lat1,lon1 = (37.443189, -122.164251) 
    lat2,lon2 = (37.455522, -122.151977)
    computed_dist = haversine(lon1,lat1,lon2,lat2)
    actual_dist = 1.1 # miles
    print 'computed distance: '+str(computed_dist)
    print 'actual distance: '+str(actual_dist)
    assert abs(computed_dist-actual_dist) < 0.05

# test in_manhattan
test_in_manhattan()
# test haversine function
test_haversine()
