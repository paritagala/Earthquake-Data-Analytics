import requests
import pandas as pd
from datetime import datetime, timedelta

# Base URL
base_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson'

# Start and end dates
start_date = datetime(2017, 1, 1)
end_date = datetime(2017, 12, 31)

# Generate list of all dates in 2017
date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Container for all earthquake data
all_earthquake_data = []

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

            earthquake_info = {
                'place': properties.get('place'),
                'time': datetime.fromtimestamp(properties.get('time') / 1000),
                'mag': properties.get('mag'),
                'longitude': geometry['coordinates'][0],
                'latitude': geometry['coordinates'][1],
                'depth': geometry['coordinates'][2]
            }

            all_earthquake_data.append(earthquake_info)
    else:
        print(f"Failed to fetch data for {single_date.strftime('%Y-%m-%d')}, status code: {response.status_code}")

# Convert to DataFrame
df = pd.DataFrame(all_earthquake_data)

# Write to Excel file
excel_file = 'earthquake_data_2017_daily.xlsx'
df.to_excel(excel_file, index=False)

print(f"Earthquake data for 2017 has been written to {excel_file}")