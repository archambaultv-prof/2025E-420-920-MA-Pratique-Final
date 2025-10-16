

#Creation de l'objet MetDatSat qui represente la meteo d'une station a une date donnee
class MetDatSat:
    def __init__(self, date, station, temperature, pressure, humidity, wind_speed, wind_direction, precipitation, cloud_cover, visibility, uv_index):
        self.date = date
        self.station = station
        self.temperature = float(temperature)
        self.pressure = float(pressure)
        self.humidity = float(humidity)
        self.wind_speed = float(wind_speed)
        self.wind_direction = float(wind_direction)
        self.precipitation = float(precipitation)
        self.cloud_cover = float(cloud_cover)
        self.visibility = float(visibility)
        self.uv_index = float(uv_index)

    # Methode pour convertir l'objet en dictionnaire
    def as_dict(self):
        return {
            "Date": self.date,
            "Station": self.station,
            "Temperature": self.temperature,
            "Pressure": self.pressure,
            "Humidity": self.humidity,
            "WindSpeed": self.wind_speed,
            "WindDirection": self.wind_direction,
            "Precipitation": self.precipitation,
            "CloudCover": self.cloud_cover,
            "Visibility": self.visibility,
            "UVIndex": self.uv_index
        }
