import csv
import threading
import time

def read_weather_data(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield {
                'date':row['Date'], 
                'station':row['Station'], 
                'temperature':float(row['Temperature']), 
                'pressure':float(row['Pressure'])
            }

def timing(func):
    lock = threading.Lock()
    def wrapper(*args, **kwargs):
        with lock:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            exec_time = time.perf_counter() - start
        return result, exec_time
    return wrapper

def compute_stats(filename):
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
        return {
            'count': 0, 
            'avg_temp': None, 
            'min_temp': None, 
            'max_temp': None, 
            'avg_pressure': None, 
            'unique_stations': 0
        }
    return {
        'count': count, 
        'avg_temp':sum(temperatures) / count, 
        'min_temp': min(temperatures), 
        'max_temp': max(temperatures), 
        'avg_pressure': sum(pressures) / count, 
        'unique_stations': len(stations)
    }

@timing
def process_files_concurrently(filenames):
    results = {}
    threads = []
    result_lock = threading.Lock()
    exec_times = {}

    def worker(filename):
        stats, exec_time = timing(compute_stats)(filename)
        with result_lock:
            results[filename] = stats
            exec_times[filename] = exec_time

    sem = threading.Semaphore(10)  # pour maximum 10 threads en meme temps

    def thread_wrapper(filename):
        with sem:
            worker(filename)

    for filename in filenames:
        t = threading.Thread(target=thread_wrapper, args=(filename, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return results, exec_times

def display_report(stats_by_file, exec_times):
    print("=== Weather Analysis Report ===\n")
    print("--- Statistics by File ---")
    for filename, stats in stats_by_file.items():
        print(f"File: {filename}")
        print(f"Processed in {exec_times[filename]:.2f}seconds")
        if stats['avg_temp'] is not None:
            print(f" Avg Temperature: {stats['avg_temp']:.1f}°C")
            print(f" Min Temperature: {stats['min_temp']:.1f}°C")
            print(f" Max Temperature: {stats['max_temp']:.1f}°C")
            print(f" Avg Pressure: {stats['avg_pressure']:.1f} hPa")
            print(f" Unique Stations: {stats['unique_stations']}")
        else:
            print(" No data in file.")
        print()

if __name__ == "__main__":
    files = [
        "data/report1.csv", 
        "data/report2.csv"
    ]
    stats_by_file, exec_times = process_files_concurrently(files)
    display_report(stats_by_file, exec_times)