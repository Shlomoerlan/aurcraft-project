from math import radians, sin, cos, sqrt, atan2
from toolz import map, filter, reduce, curry, pipe
from models.assigned_target import Assigned_target
from operator import itemgetter
from functools import reduce
import random
import json


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def suitable_aircrafts(distance, aircrafts):
    return list(filter(lambda ac: ac['fuel_capacity'] >= distance, aircrafts))


def weather_score(city_weather):
    weather, clouds, wind_speed = itemgetter('weather', 'clouds', 'wind_speed')(city_weather)

    if weather == "Clear":
        weather_score = 20
    elif weather == "Clouds":
        weather_score = 18
    elif weather == "Rain":
        weather_score = 15
    else:
        weather_score = 12

    clouds_score = 20 - (clouds / 4)
    wind_score = 20 - (wind_speed / 3)

    total_score = (weather_score + clouds_score + wind_score) / 3

    return total_score


def calculate_distance_score(distance, max_distance, min_distance):
    return 20 if distance == min_distance else max(10, 20 - ((distance - min_distance) / (max_distance - min_distance)) * 10)

def calculate_aircraft_score(aircraft_type):
    scores = {
        "Fighter Jet": 25, "Stealth Fighter": 23, "Bomber": 20,
        "Heavy Bomber": 19, "Recon Drone": 17, "Drone": 15, "Helicopter": 13
    }
    return scores.get(aircraft_type, 13)

def calculate_weighted_score(distance_score, aircraft_score, pilot_skill, weather_score, execution_time_score):
    return (0.20 * distance_score) + (0.25 * aircraft_score) + (0.25 * pilot_skill) + (0.20 * weather_score) + (
            0.10 * execution_time_score)

def create_assigned_target(city, priority, pilot, distance, weather, pilot_skill, aircraft_speed, fuel_capacity, aircraft_type ,  mission_fit_score):
    return Assigned_target(city, priority, pilot, distance, weather, pilot_skill, aircraft_speed, fuel_capacity,aircraft_type, mission_fit_score)

def random_multiply_score(item):
    multiplier = random.uniform(1, 3.5)
    item.mission_fit_score *= multiplier
    return item

@curry
def assign_target(pilot, aircraft, city_name, priority, distance, city_weather, max_distance, min_distance):
    pilot_skill = pilot["skill"] * 2.5
    aircraft_score = calculate_aircraft_score(aircraft["type"])
    distance_score = calculate_distance_score(distance, max_distance, min_distance)
    weather_score_value = weather_score(city_weather)
    execution_time_score = distance_score
    aircraft_type = aircraft['type']
    mission_fit_score = calculate_weighted_score(distance_score, aircraft_score, pilot_skill, weather_score_value, execution_time_score)
    return create_assigned_target(city_name, priority, pilot["name"], distance, city_weather["weather"], pilot_skill, aircraft["speed"], aircraft["fuel_capacity"], aircraft_type, mission_fit_score)


def get_distances(cities, tel_aviv):
    return map(lambda city: (city[0], calculate_distance(tel_aviv['lat'], tel_aviv['lon'], city[1]['lat'], city[1]['lon'])), cities.items())


def generate_assigned_targets():
    tel_aviv = {"lat": 32.0833, "lon": 34.8}
    pilots = load_json("../assets/pilots.json")
    aircrafts = load_json("../assets/aircraft.json")
    cities = load_json("../assets/cities.json")
    targets = load_json("../assets/targets.json")

    distances = dict(get_distances(cities, tel_aviv))
    max_distance = max(distances.values())
    min_distance = min(distances.values())

    assign_target_partial = assign_target(max_distance=max_distance, min_distance=min_distance)

    assigned_targets = list(pipe(
        targets,
        lambda targets: list(map(lambda target: (
            target['city'],
            target['priority'],
            distances.get(target['city']),
            cities.get(target['city'])
        ), targets)),
        lambda t: [assign_target_partial(pilot, aircraft, city_name, priority, distance, city_weather)
                   for city_name, priority, distance, city_weather in t
                   for aircraft in suitable_aircrafts(distance, aircrafts)
                   for pilot in pilots]
    ))

    assigned_targets_with_random_scores = list(map(random_multiply_score, assigned_targets))
    save_json(assigned_targets_with_random_scores, "../assets/assigned_updated.json")


def save_json(data, path):
    with open(path, 'w') as json_file:
        json.dump([ob.__dict__ for ob in data], json_file, indent=4)


def get_top_5_targets(data):
    sorted_data = sorted(data, key=lambda x: x.mission_fit_score, reverse=True)
    return sorted_data[:5]


def is_unique_target(target, used_pilots, used_aircrafts, used_cities):
    pilot = target['assigned_pilot']
    aircraft = target['aircraft_type']
    city = target['target_city']
    return pilot not in used_pilots and aircraft not in used_aircrafts and city not in used_cities


def add_target(acc, target):
    used_pilots, used_aircrafts, used_cities, top_targets = acc
    if is_unique_target(target, used_pilots, used_aircrafts, used_cities):
        top_targets.append(target)
        used_pilots.add(target['assigned_pilot'])
        used_aircrafts.add(target['aircraft_type'])
        used_cities.add(target['target_city'])
    return used_pilots, used_aircrafts, used_cities, top_targets


def get_top_7_unique_targets(assigned_targets):
    sorted_targets = sorted(assigned_targets, key=itemgetter('mission_fit_score'), reverse=True)
    _, _, _, top_targets = reduce(add_target, sorted_targets, (set(), set(), set(), []))
    return top_targets[:7]


generate_assigned_targets()
assigned = load_json("../assets/assigned_updated.json")
print(len(assigned))
# top_5 = get_top_5_targets([Assigned_target(**item) for item in assigned])

f = get_top_7_unique_targets(assigned)
for i in f:
    print(i['target_city'], i['assigned_pilot'], i['aircraft_type'])
