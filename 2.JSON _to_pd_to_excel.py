#Step1: pip install requests in the terminal
#Step2: pip install pandas library
#Step 3: 
import pandas as pd
import requests

# API URL for earthquake data
url = 'https://earthquake.usgs.gov/fdsnws/event/1/application.json'

# Fetch data from the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse JSON response
    data = response.json()

    # Extract earthquake data
    event_types = data.get('eventtypes', [])
    magnitude_types = data.get('magnitudetypes', [])
    catalogs = data.get('catalogs', [])
    contributors = data.get('contributors', [])
    product_types = data.get('producttypes', [])

    # Ensure all arrays have the same length
    max_length = max(len(event_types), len(magnitude_types), len(catalogs), len(contributors), len(product_types))
    event_types += [''] * (max_length - len(event_types))
    magnitude_types += [''] * (max_length - len(magnitude_types))
    catalogs += [''] * (max_length - len(catalogs))
    contributors += [''] * (max_length - len(contributors))
    product_types += [''] * (max_length - len(product_types))

    # Create DataFrame
    df = pd.DataFrame({
        'Event Types': event_types,
        'Magnitude Types': magnitude_types,
        'Catalogs': catalogs,
        'Contributors': contributors,
        'Product Types': product_types
    })

    # Write DataFrame to Excel file
    excel_file = 'earthquake_data.xlsx'
    df.to_excel(excel_file, index=False)

    print(f'Earthquake data has been written to {excel_file}')
else:
    print(f'Failed to fetch data from the API. Status code: {response.status_code}')
