import pandas as pd

# Define file paths
user_profile_nyc_path = 'dataset_UbiComp2016_UserProfile_NYC.txt'
user_profile_tky_path = 'dataset_UbiComp2016_UserProfile_TKY.txt'
checkin_nyc_path = 'checkin_NYC.tsv'
checkin_tky_path = 'checkin_TKY.tsv'

# Load User Profile Data
# Assuming tab-separated values
user_profile_nyc = pd.read_csv(user_profile_nyc_path, sep='\t', header=None, 
                              names=['User ID', 'Gender', 'TwitterFriendCount', 'TwitterFollowerCount'])
user_profile_tky = pd.read_csv(user_profile_tky_path, sep='\t', header=None, 
                              names=['User ID', 'Gender', 'TwitterFriendCount', 'TwitterFollowerCount'])

user_profiles = pd.concat([user_profile_nyc, user_profile_tky], ignore_index = True)

# Load Check-in Data
metrics = pd.read_csv("user_locations_with_metrics.csv")
combined_data = metrics.merge(user_profiles, how = 'inner', on = 'User ID')

# Save the Merged Data to a New File
combined_data.to_csv('dmerged_user_checkin_data.csv', index=False)
