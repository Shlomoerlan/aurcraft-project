import requests
import math
import json

API_KEY = 'd1b36048815a3b848dacff1f6e511b62'
target_datetime = "2024-09-13 00:00:00"


def get_city_coordinates(city_name):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            city_info = data[0]
            lat = city_info.get('lat')
            lon = city_info.get('lon')
            return {"lat": lat, "lon": lon}
        else:
            return "City not found"
    else:
        return f"Error {response.status_code}: {response.text}"


def get_weather_data_for_city(city_name):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        target_datetime = "2024-09-13 00:00:00"

        for entry in data['list']:
            if entry['dt_txt'] == target_datetime:
                weather_main = entry['weather'][0]['main']
                clouds_all = entry['clouds']['all']
                wind_speed = entry['wind']['speed']
                return {
                    "weather": weather_main,
                    "clouds": clouds_all,
                    "wind_speed": wind_speed
                }
        return "No data found for the target date"
    else:
        return f"Error {response.status_code}: {response.text}"


def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371.0
    # Radius of the Earth in kilometers #
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    # Calculate differences between the coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    # Apply Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Calculate the distance
    distance = r * c
    return distance


def get_city_data(city_name):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        city_info = {
            "lat": data['city']['coord']['lat'],
            "lon": data['city']['coord']['lon']
        }


        for entry in data['list']:
            if entry['dt_txt'] == target_datetime:
                city_info["weather"] = entry['weather'][0]['main']
                city_info["clouds"] = entry['clouds']['all']
                city_info["wind_speed"] = entry['wind']['speed']
                break

        return {city_name: city_info}
    else:
        print(f"Error fetching data for {city_name}: {response.status_code}")
        return None



cities = [
    "Tel Aviv",
    "Damascus", "Beirut", "Amman", "Cairo", "Baghdad", "Tehran",
    "Riyadh", "Tripoli", "Ankara", "Khartoum", "Sanaa",
    "Manama", "Kuwait City", "Doha"
]


city_data_dict = {}
for city in cities:
    city_data = get_city_data(city)
    if city_data:
        city_data_dict.update(city_data)


with open('../assets/cities.json', 'w') as json_file:
    json.dump(city_data_dict, json_file, indent=4)





