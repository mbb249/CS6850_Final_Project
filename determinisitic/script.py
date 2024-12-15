import csv

# Read the data from the text file
input_file = "edges_locations.txt"
output_file = "locations.csv"
4
# Create a dictionary to store unique rounded positions for each user_id
data = {}

with open(input_file, "r") as file:
    for line in file:
        user_id, timestamp, latitude, longitude, _ = line.split()
        user_id = int(user_id)
        latitude = round(float(latitude), 2)
        longitude = round(float(longitude), 2)

        if user_id not in data:
            data[user_id] = set()

        data[user_id].add((latitude, longitude))

# Write the data to a CSV file
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["user_id", "positions"])

    for user_id, positions in data.items():
        writer.writerow([user_id, list(positions)])

print(f"Data has been successfully written to {output_file}")
