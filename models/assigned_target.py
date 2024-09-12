class Assigned_target:
    def __init__(self, target_city, priority, assigned_pilot, distance, weather_condition, pilot_skill, aircraft_speed, fuel_capacity, aircraft_type,  mission_fit_score):
        self.target_city = target_city
        self.priority = priority
        self.assigned_pilot = assigned_pilot
        self.distance = distance
        self.weather_condition = weather_condition
        self.pilot_skill = pilot_skill
        self.aircraft_speed = aircraft_speed
        self.aircraft_type = aircraft_type
        self.fuel_capacity = fuel_capacity

        self.mission_fit_score = mission_fit_score

    def __repr__(self):
        return (f"Target City: {self.target_city}, Priority: {self.priority}, Pilot: {self.assigned_pilot}, "
                f"Distance: {self.distance}km, Weather: {self.weather_condition}, "
                f"Pilot Skill: {self.pilot_skill}, Aircraft Speed: {self.aircraft_speed}km/h, "
                f"Fuel Capacity: {self.fuel_capacity} liters, Mission Fit Score: {self.mission_fit_score}")
