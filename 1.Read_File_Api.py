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
    #Step 7: And print data
    print(f"Found data, status code:{response.status_code}")

#Step 8: Else print failed to find the data
else: 
    print(f"Failed to find data, status code:{response.status_code}")


