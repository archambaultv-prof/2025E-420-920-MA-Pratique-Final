import time
import threading
import concurrent.futures
from statistics import mean


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


# Décorateur thread-safe pour mesurer le temps d'exécution
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


def compute_statistics(records):
    """Calcule les statistiques de base pour un fichier."""
    temps = [r["temperature"] for r in records]
    pressions = [r["pressure"] for r in records]
    stations = {r["station"] for r in records}

    return {
        "records": len(records),
        "avg_temp": round(mean(temps), 2),
        "min_temp": round(min(temps), 2),
        "max_temp": round(max(temps), 2),
        "avg_pressure": round(mean(pressions), 2),
        "unique_stations": len(stations),
    }


def process_file(filename):
    """Lit un fichier et retourne ses statistiques."""
    records = list(read_weather_data(filename))
    return compute_statistics(records)


def process_files_concurrently(filenames):
    """Traite plusieurs fichiers CSV en parallèle (max 10 threads)."""
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_file = {executor.submit(process_file, f): f for f in filenames}

        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                results[file] = future.result()
            except Exception as e:
                results[file] = {"error": str(e)}

    return results


@timing
def main():
    """Analyse plusieurs fichiers CSV en parallèle."""
    files = ["../data/report1.csv", "../data/report2.csv", "../data/report3.csv"]
    return process_files_concurrently(files)


if __name__ == "__main__":
    results, exec_time = main()

    print("=== Résultats de l'analyse concurrente ===")
    print(f"Temps total : {exec_time} secondes\n")

    for file, stats in results.items():
        print(f"Fichier : {file}")
        if "error" in stats:
            print(f"  Erreur : {stats['error']}")
        else:
            print(f"  Lectures : {stats['records']}")
            print(f"  Température moyenne : {stats['avg_temp']}°C")
            print(f"  Min : {stats['min_temp']}°C | Max : {stats['max_temp']}°C")
            print(f"  Pression moyenne : {stats['avg_pressure']} hPa")
            print(f"  Stations uniques : {stats['unique_stations']}")
        print()