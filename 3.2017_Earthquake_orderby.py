import requests
import pandas as pd
from datetime import datetime

# URL to fetch earthquake data in GeoJSON format
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2017-01-01&endtime=2017-12-31&orderby=magnitude&limit=5000'

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
        geometry = feature['geometry']
        
        # Convert the timestamp to a datetime object
        timestamp = properties.get('time')
        date_time = datetime.fromtimestamp(timestamp / 1000)  # Convert milliseconds to seconds

        # Check if the year is 2017
        if date_time.year == 2017:
            earthquake_info = {
                'place': properties.get('place'),
                'time': date_time,
                'updated': datetime.fromtimestamp(properties.get('updated') / 1000) if properties.get('updated') else None,
                'mag': properties.get('mag'),
                'felt': properties.get('felt'),
                'cdi': properties.get('cdi'),
                'mmi': properties.get('mmi'),
                'alert': properties.get('alert'),
                'status': properties.get('status'),
                'tsunami': properties.get('tsunami'),
                'sig': properties.get('sig'),
                'net': properties.get('net'),
                'code': properties.get('code'),
                'ids': properties.get('ids'),
                'sources': properties.get('sources'),
                'types': properties.get('types'),
                'nst': properties.get('nst'),
                'dmin': properties.get('dmin'),
                'rms': properties.get('rms'),
                'gap': properties.get('gap'),
                'magType': properties.get('magType'),
                'type': properties.get('type'),
                'longitude': geometry['coordinates'][0],
                'latitude': geometry['coordinates'][1],
                'depth': geometry['coordinates'][2]
            }

            earthquake_data.append(earthquake_info)

    # Step 3: Convert to a pandas DataFrame
    df = pd.DataFrame(earthquake_data)

    # Step 4: Write the DataFrame to an Excel file
    excel_file = 'earthquake_data_2017.xlsx'
    df.to_excel(excel_file, index=False)

    print(f"Earthquake data for 2017 has been written to {excel_file}")
else:
    print(f"Failed to fetch data, status code: {response.status_code}")