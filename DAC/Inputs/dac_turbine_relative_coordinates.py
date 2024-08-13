# Importing the geodesic module from the library 
from geopy.distance import geodesic 
import pandas as pd
import numpy as np
  
# Northeastern most point 
Northeast = (34.26, -101.27)

# read csv file of coordinates
df = pd.read_csv('HOPP/DAC/Inputs/SouthPlainsII_Turbine_Coordinates.csv')

# separate latitude and longitdue
latitudes = df.lat
longitudes = df.long

# find distance from Northeastern most point in the x-direction 
x_distance = []
set_lat = 34.26
for long in longitudes:
    coords = np.array([set_lat, long])
    dist = geodesic(coords, Northeast).m
    x_distance.append(dist)

# find distance from Northeastern most point in the y-direction
y_distance = []
set_long = -101.27
for lat in latitudes:
    coords = np.array([lat, set_long])
    dist = geodesic(coords, Northeast).m
    y_distance.append(dist)

new_coordinates = np.array([x_distance, y_distance])

new_df = pd.DataFrame(np.transpose(new_coordinates))
# new_df.to_csv('turbine_coordinates_southplainsii.csv', index=False)


helpme = pd.DataFrame(np.transpose(x_distance))
helpme.to_csv('x_coordinatesforstudy.csv')