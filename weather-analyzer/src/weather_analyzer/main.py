import csv
import threading
import time
from functools import wraps
from pathlib import Path

lock = threading.Lock()
def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        with lock:
            return result, end - start
    return wrapper

def read_weather_data(filename):
    """Générateur pour lire les fichiers CSV ligne par ligne"""
    with open(filename, newline='', encoding='utf-16') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {
                'date': row['Date'],
                'station': row['Station'],
                'temperature': float(row['Temperature']),
                'pressure': float(row['Pressure'])
            }


def record_statistics(filename):
    temperatures = []
    pressures = []
    stations = set()
    count = 0

    for row in read_weather_data(filename):
        temperatures.append(row['temperature'])
        pressures.append(row['pressure'])
        stations.add(row['station'])
        count += 1

    if count == 0:
        return None

    return {
        'records': count,
        'avg_temp': sum(temperatures)/count,
        'min_temp': min(temperatures),
        'max_temp': max(temperatures),
        'avg_pressure': sum(pressures)/count,
        'unique_stations': len(stations)
    }

# threading 
def process_files_concurrently(filenames):
    results = {}
    threads = []

    def worker(file):
        stats, exec_time = timing(record_statistics)(file)
        results[file] = (stats, exec_time)

    for file in filenames[:7]:  
        t = threading.Thread(target=worker, args=(file,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results
    
#fonction principale
def main():
    # Chemin vers le dossier 'data' 
    data_dir = Path(__file__).resolve().parent.parent.parent.parent / "data"

    # Liste des fichiers CSV
    filenames = sorted(data_dir.glob("report*.csv"))

    if not filenames:
        print(f"Aucun fichier CSV trouvé dans {data_dir}")
        return

    all_results = process_files_concurrently(filenames)

    print("\n=== Weather Analysis Report ===\n")
    for file, (stats, exec_time) in all_results.items():
        if stats is None:
            print(f"File: {file} - aucun enregistrement")
            continue
        print(f"File: {file}")
        print(f"Processed in {exec_time:.2f} seconds")
        print(f"  Records: {stats['records']}")
        print(f"  Avg Temperature: {stats['avg_temp']:.1f}°C")
        print(f"  Min Temperature: {stats['min_temp']:.1f}°C")
        print(f"  Max Temperature: {stats['max_temp']:.1f}°C")
        print(f"  Avg Pressure: {stats['avg_pressure']:.1f} hPa")
        print(f"  Unique Stations: {stats['unique_stations']}\n")

if __name__ == "__main__":
    main()
