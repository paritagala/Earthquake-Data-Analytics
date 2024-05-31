import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Base URL
base_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson'

# Start and end dates
start_date = datetime(2017, 1, 1)
end_date = datetime(2017, 12, 31)

# Generate list of all dates in 2017
date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Container for all earthquake data
earthquake_data = []

# Fetch data for each day
for single_date in date_list:
    start_time = single_date.strftime('%Y-%m-%dT00:00:00')
    end_time = (single_date + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00')
    
    url = f"{base_url}&starttime={start_time}&endtime={end_time}&orderby=magnitude"
    
    # Make the HTTP request
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        features = data.get('features', [])
        
        for feature in features:
            properties = feature['properties']
            geometry = feature['geometry']

            # Convert the timestamp to a datetime object
            timestamp = properties.get('time')
            date_time = datetime.fromtimestamp(timestamp / 1000)  # Convert milliseconds to seconds

            # Extract the magnitude and hour of the day
            magnitude = properties.get('mag')
            hour_of_day = date_time.hour

            earthquake_info = {
                'magnitude': magnitude,
                'hour_of_day': hour_of_day
            }

            earthquake_data.append(earthquake_info)
    else:
        print(f"Failed to fetch data for {single_date.strftime('%Y-%m-%d')}, status code: {response.status_code}")

# Step 2: Convert to a pandas DataFrame
df = pd.DataFrame(earthquake_data)

# Step 3: Define magnitude buckets
bins = [0, 1, 2, 3, 4, 5, 6, np.inf]
labels = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '>6']
df['mag_binned'] = pd.cut(df['magnitude'], bins=bins, labels=labels, right=False)

# Step 4: Calculate the most probable hour of the day for each bucket
results = []

for cat in labels:
    cat_data = df[df['mag_binned'] == cat]['hour_of_day']
    if not cat_data.empty:
        hour_mode = int(cat_data.mode()[0])
        hour_mode_counts = cat_data.value_counts().max()
        results.append({'Magnitude Category': cat, 'Most Probable Hour': hour_mode, 'Count': hour_mode_counts})
        print('For magnitude category {} the most probable hour of the day for an earthquake is {} with {} recorded events.'.format(cat, hour_mode, hour_mode_counts))
    else:
        results.append({'Magnitude Category': cat, 'Most Probable Hour': None, 'Count': 0})
        print('For magnitude category {} there are no recorded events.'.format(cat))

# Step 5: Convert the results to a DataFrame
results_df = pd.DataFrame(results)

# Step 6: Write the results to an Excel file
excel_file = 'most_probable_hour_by_magnitude_2017.xlsx'
results_df.to_excel(excel_file, index=False)

print(f"The most probable hour of the day for each magnitude range in 2017 has been written to {excel_file}")
