#Step 1 : Pip install requests in the terminal
#Step 2: Import requests below

import requests

#Step 3: Define the url of the API : in other words give a name to the API

url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson'

#Step 4: Find the data from the API. This is when I used the comman "request get"

response = requests.get(url)

#Step 5: Checking if the request was successful it will return the status code 200
if response.status_code == 200:
    # Step 6: If the status code is 200 the parse the json response
    data = response.json()
    #Step 7: And print data
    print(data)

#Step 8: Else print failed to find the data
else: 
    print(f"Failed to find data, status code:{response.status_code}")


