from operator import itemgetter

class Mission:
    def __init__(self, target_name, distance, weather_conditions, aircraft, pilot, execution_time):
        self.target_name = target_name
        self.distance = distance
        self.weather_conditions = weather_conditions
        self.aircraft = aircraft
        self.pilot = pilot
        self.execution_time = execution_time

    def weather_score(self):
        condition = itemgetter('condition')(self.weather_conditions)
        return {
            "Clear": 1.0,
            "Clouds": 0.7,
            "Rain": 0.4,
            "Stormy": 0.2
        }.get(condition, 0)


    def __repr__(self):
        return f"Mission to {self.target_name}, Weather: {self.weather_conditions}, Aircraft: {self.aircraft}, Pilot: {self.pilot}"
