import requests

API_KEY = 'd1b36048815a3b848dacff1f6e511b62'

class WeatherAPI:
    @staticmethod
    def get_weather_forecast(city):
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None


class JsonRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        return pipe(
            self.file_path,
            lambda path: open(path, 'r'),
            json.load
        )

    def save_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

