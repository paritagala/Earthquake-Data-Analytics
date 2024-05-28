import requests
import pandas as pd
from datetime import datetime

# URL to fetch earthquake data in GeoJSON format
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2017-01-01&endtime=2017-12-31&limit=20000'

# Step 1: Fetch the GeoJSON data from the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Step 2: Parse the GeoJSON data
    # Extract relevant information from each earthquake feature
    features = data['features']
    earthquake_data = []

    for feature in features:
        properties = feature['properties']
        
        # Convert the timestamp to a datetime object
        timestamp = properties.get('time')
        date_time = datetime.utcfromtimestamp(timestamp / 1000)  # Convert milliseconds to seconds

        # Extract magnitude and hour of the day
        magnitude = properties.get('mag')
        hour_of_day = date_time.hour

        if magnitude is not None:  # Check if magnitude is available
            earthquake_info = {
                'magnitude': magnitude,
                'hour_of_day': hour_of_day
            }

            earthquake_data.append(earthquake_info)

    # Step 3: Create buckets for magnitude ranges
    magnitude_buckets = {
        '0-1': (0, 1),
        '1-2': (1, 2),
        '2-3': (2, 3),
        '3-4': (3, 4),
        '4-5': (4, 5),
        '5-6': (5, 6),
        '>6': (6, float('inf'))
    }

    # Step 4: Count earthquakes in each hour for each magnitude range
    hour_counts = {}

    for bucket_name, (lower_limit, upper_limit) in magnitude_buckets.items():
        # Filter earthquakes within the magnitude range
        filtered_earthquakes = [earthquake['hour_of_day'] for earthquake in earthquake_data if earthquake['magnitude'] is not None and lower_limit <= earthquake['magnitude'] < upper_limit]
        # Count occurrences of each hour
        hour_counts[bucket_name] = {hour: filtered_earthquakes.count(hour) for hour in range(24)}

    # Step 5: Convert the results to a DataFrame and write to Excel
    df = pd.DataFrame(hour_counts)
    excel_file = 'earthquake_hourly_analysis.xlsx'
    df.to_excel(excel_file)

    print(f"Hourly analysis of earthquakes by magnitude range has been written to {excel_file}")
else:
    print(f"Failed to fetch data, status code: {response.status_code}")
