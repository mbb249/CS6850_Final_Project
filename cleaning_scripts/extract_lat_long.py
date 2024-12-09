import pandas as pd

# Define the column names
columns = ["Venue ID", "Latitude", "Longitude", "Venue category", "Country code"]

# Load the text file into a DataFrame
df = pd.read_csv('raw_POIs.txt', sep='\t', header=None, names=columns)

# Select only the required columns: Venue ID, Latitude, and Longitude
venue_data = df[["Venue ID", "Latitude", "Longitude"]]

# Display the resulting DataFrame
print(venue_data.head())

# Optionally, save the extracted data to a new file
venue_data.to_csv('venue_coordinates.csv', index=False)
