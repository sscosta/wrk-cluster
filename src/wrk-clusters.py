
import pandas as pd
import requests
import time
import folium
from folium.plugins import MarkerCluster
from collections.abc import Iterable

in_path = '../data/companies.csv'
out_path = '../data/companies_enriched.csv'

def get_company_data(company_name):
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': f"{company_name}, Lisbon, Portugal",
        'key': "YOUR_API_KEY_HERE"
    }
    response = requests.get(url, params=params)
    print(company_name)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            address = data['results'][0]['formatted_address']
            latitude = location['lat']
            longitude = location['lng']
            return address, latitude, longitude
    return 'Unknown', None, None

companies = pd.read_csv(in_path)

addresses = []
latitudes = []
longitudes = []

for index, row in companies.iterrows():
    name = row['Company']
    address, lat, lon = get_company_data(name)
    addresses.append(address)
    latitudes.append(lat)
    longitudes.append(lon)
    #time.sleep(1)

companies['Address'] = addresses
companies['Latitude'] = latitudes
companies['Longitude'] = longitudes

companies.to_csv(out_path, index=False)

map_center = [38.736946, -9.142685]
map_folium_1 = folium.Map(location=map_center, zoom_start=12, tiles='CartoDB dark_matter')

marker_cluster = MarkerCluster().add_to(map_folium_1)

for _, company in companies.iterrows():
    if pd.notnull(company['Latitude']) and pd.notnull(company['Longitude']):
        folium.Marker(
            location=[company['Latitude'], company['Longitude']],
            popup=f"<b>{company['Company']}</b><br>Address: {company['Address']}<br>Employees: {company['Num_Employees']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(marker_cluster)

map_folium_1.save(out_path.replace('.csv', '_map_with_clusters.html'))

map_folium_2 = folium.Map(location=map_center, zoom_start=12, tiles='CartoDB dark_matter')

for _, company in companies.iterrows():
    if pd.notnull(company['Latitude']) and pd.notnull(company['Longitude']):
        folium.CircleMarker(
            location=[company['Latitude'], company['Longitude']],
            radius=company['Num_Employees'] / 1000,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            popup=f"<b>{company['Company']}</b><br>Employees: {company['Num_Employees']}"
        ).add_to(map_folium_2)

map_folium_2.save(out_path.replace('.csv', '_map_with_workers.html'))

print('Two Folium maps created and saved in dark mode.')
