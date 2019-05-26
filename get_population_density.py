import pandas as pd
from math import cos, asin, sqrt

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def population_den(lat,long):
    df = pd.read_csv("/Users/2020shatgiskessell/Desktop/Missing_Child_Recognition/cities15000.csv",encoding = "ISO-8859-1")
    #print(df.head(5))
    populations = list(df['population'])
    name = list(df['name'])
    longitudes = list(df['longitude'])
    latitudes = list(df['latitude'])
    min_dist = 100000000
    index = 0
    for lat1, long1 in zip(latitudes,longitudes):
    # if type(lat1) == int and type(lat2) == int:
        try:
            dist = distance(float(lat1), float(long1), float(lat), float(long))
        except ValueError:
            continue
        #     print (dist)
        # else:
        #     continue
        if dist < min_dist:
            min_dist = dist
            index = latitudes.index(lat1)
    # print ("popultion: " + str(populations[index]))
    # print ("country: " + str(name[index]))
    return populations[index], name[index]
