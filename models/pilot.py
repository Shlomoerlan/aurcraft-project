class Pilot:
    def __init__(self, name, skill):
        self.name = name
        self.skill = skill

    def __repr__(self):
        return f"Name: {self.name}, Skill: {self.skill}"



key1 = "http://api.openweathermap.org/geo/1.0/direct?q=teheran&appid=d1b36048815a3b848dacff1f6e511b62"
key2 ="https://api.openweathermap.org/data/2.5/forecast?q=yemen&appid=d1b36048815a3b848dacff1f6e511b62"