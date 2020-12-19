'''
Created on Oct 29, 2019

@author: Shan Wu
'''

import googlemaps
import pandas as pd
import json
from pathlib import Path
from numpy.compat.py3k import PurePath
import unidecode as ud


site_column = "site"
country_column = "country"

gmaps = googlemaps.Client(key='AIzaSyCVICwt415erbiRgY4lIwvuSt6mfcKAums')
lat_list = []
lng_list = []
site_list = []

'''
geocode_result = gmaps.find_place('Sandia National Laboratories, United States', 'textquery')
#print(geocode_result)
#if len(geocode_result) == 0:
 #   print("Here")
#else:
 #   result = geocode_result[0]
#print(geocode_result)
print(len(geocode_result['candidates']))
#result = gmaps.place(geocode_result['candidates'][0]['place_id'])
#print(result['result']['name'])
#print(result['result']['geometry']['location']['lat'])
#result-geometry-location-lat/lng
#result-name
'''



#read each line of the super500.csv file
p = PurePath(r"C:\Users\Shan Wu\Desktop\super500_1.csv")
data = pd.read_csv(p, low_memory=False)

#retrieve the site and country column from the csv file
#put the information from the 2 columns together to form
#a list of address
addresses = (data[site_column] + ',' + data[country_column]).tolist()

#put each addresses into the google map API to find the
#place(scraping)
for address in addresses:
    #use the find_place function to run the sites through Google Map and get the name
    #of the site, the longitude and the latitude
    place_result = gmaps.find_place(address, 'textquery')
    numResult = len(place_result['candidates'])
    #if only one place is fouond
    if numResult == 1:
        result = gmaps.place(place_result['candidates'][0]['place_id'])
        site = result['result']['name']
        lat = result['result']['geometry']['location']['lat']
        long = result['result']['geometry']['location']['lng']
        clean_site = ud.unidecode(site)
        site_list.append(clean_site)
        lat_list.append(lat)
        lng_list.append(long)
    #if no such sites are found
    elif numResult == 0:
        site_list.append("")
        lat_list.append("")
        lng_list.append("")
    #if more than one results are found
    else:
        site_list.append("")
        lat_list.append("")
        lng_list.append("")

#write to the csv file
data['latitude'] = lat_list
data['longitude'] = lng_list
data['site'] = site_list
data.to_csv(r"C:\Users\Shan Wu\Desktop\super500_1.csv", index=False)



