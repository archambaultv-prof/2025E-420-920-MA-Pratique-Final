def read_weather_data(filename):
    """Lit un fichier CSV météo et renvoie un dictionnaire par ligne."""
    with open(filename, "r", encoding="utf-16") as f:
        next(f)  # sauter l'en-tête
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 4:
                continue
            date, station, temperature, pressure = parts
            yield {
                "date": date,
                "station": station,
                "temperature": float(temperature),
                "pressure": float(pressure)
            }


def main():
    for record in read_weather_data("../data/report1.csv"):
        print(record)


if __name__ == "__main__":
    main()