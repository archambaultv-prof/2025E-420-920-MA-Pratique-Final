import time
import threading


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


# Décorateur thread-safe pour mesurer le temps d'exécution d'une fonction
def timing(func):
    lock = threading.Lock()

    def wrapper(*args, **kwargs):
        with lock:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            exec_time = round(end - start, 4)
            return result, exec_time

    return wrapper


@timing
def main():
    """Test du générateur avec mesure du temps d'exécution."""
    records = list(read_weather_data("../data/report1.csv"))
    return records


if __name__ == "__main__":
    data, exec_time = main()
    print(f"Analyse terminée en {exec_time} secondes")
    for record in data[:5]:
        print(record)