import pandas as pd

venues = pd.read_csv("venue_coordinates.csv")
checkin_locations = pd.read_csv("first_checkin_locations.csv")


df = pd.merge(venues, checkin_locations, how = 'inner', on = 'Venue ID')[['User ID', 'Latitude', 'Longitude']]
print(df.head(20))

df.to_csv("user_locations.csv", index =False)