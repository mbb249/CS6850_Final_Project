import pandas as pd

columns = ["User ID", "Venue ID", "UTC time", "Timezone offset"]
df = pd.read_csv('raw_Checkins_anonymized.txt', sep='\t', header=None, names=columns)
print(len(df.index))
unique_users_df = df.drop_duplicates(subset="User ID", keep="first")
print(len(unique_users_df.index))
unique_users_df.to_csv('first_checkin_locations.csv', index=False)
