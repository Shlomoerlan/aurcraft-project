import json
from toolz import pipe
from models.pilot import Pilot
from models.aircraft import Aircraft
from models.mission import Mission
from models.target import Target


def read_aircraft_from_json(filename: str):
    data = read_json(filename)
    return [convert_from_json_to_aircraft(aircraft) for aircraft in data]

def read_json(path: str):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return []

def convert_from_json_to_aircraft(aircraft_data: dict):
    return Aircraft(
        type=aircraft_data["type"],
        fuel_capacity=aircraft_data["fuel_capacity"],
        speed=aircraft_data["speed"]
    )

def read_pilots_from_json(filename: str) -> list[Pilot]:
    data = read_json(filename)
    return [convert_from_json_to_pilot(pilot) for pilot in data]

def convert_from_json_to_pilot(pilot_data: dict) -> Pilot:
    return Pilot(
        name=pilot_data["name"],
        skill=pilot_data["skill"]
    )

def read_targets_from_json(filename: str):
    data = read_json(filename)
    return [convert_from_json_to_target(target) for target in data]

def convert_from_json_to_target(target_data: dict):
    return Target(
        city=target_data["city"],
        priority=target_data["priority"]
    )