import csv
import time
from pathlib import Path
from threading import Thread, Lock

# Décorateur @timing thread-safe

def timing(func):
    lock = Lock()
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        with lock:
            exec_time = end - start
        return result, exec_time
    return wrapper

# Générateur pour lire les CSV ligne par ligne

def read_weather_data(filename):
    with open(filename, 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {
                "date": row["Date"],
                "station": row["Station"],
                "temperature": float(row["Temperature"]),
                "pressure": float(row["Pressure"])
            }

# Calcul statistiques pour un fichier

@timing
def compute_statistics(filename):
    temperatures = []
    pressures = []
    stations = set()
    records = 0

    for record in read_weather_data(filename):
        temperatures.append(record["temperature"])
        pressures.append(record["pressure"])
        stations.add(record["station"])
        records += 1

    if records == 0:
        return {
            "records": 0,
            "avg_temp": None,
            "min_temp": None,
            "max_temp": None,
            "avg_pressure": None,
            "unique_stations": 0
        }

    return {
        "records": records,
        "avg_temp": sum(temperatures) / records,
        "min_temp": min(temperatures),
        "max_temp": max(temperatures),
        "avg_pressure": sum(pressures) / records,
        "unique_stations": len(stations)
    }

# Traitement multi-thread

def process_files_concurrently(filenames):
    results = {}
    threads = []
    lock = Lock()

    def worker(file):
        stats, exec_time = compute_statistics(file)
        with lock:
            results[file] = (stats, exec_time)

    for file in filenames[:10]:  # maximum 10 threads
        t = Thread(target=worker, args=(file,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results


# Affichage des résultats

def display_results(results):
    print("=== Weather Analysis Report ===\n")
    print("--- Statistics by File ---")
    for file, (stats, exec_time) in results.items():
        print(f"File: {file}")
        print(f"Processed in {exec_time:.2f} seconds")
        print(f"  Records: {stats['records']}")
        if stats['records'] > 0:
            print(f"  Avg Temperature: {stats['avg_temp']:.1f}°C")
            print(f"  Min Temperature: {stats['min_temp']:.1f}°C")
            print(f"  Max Temperature: {stats['max_temp']:.1f}°C")
            print(f"  Avg Pressure: {stats['avg_pressure']:.1f} hPa")
            print(f"  Unique Stations: {stats['unique_stations']}")
        print("")

# Fonction main

def main():
    data_folder = Path("../data")
    csv_files = sorted(data_folder.glob("report*.csv"))
    results = process_files_concurrently(csv_files)
    display_results(results)

if __name__ == "__main__":
    main()
