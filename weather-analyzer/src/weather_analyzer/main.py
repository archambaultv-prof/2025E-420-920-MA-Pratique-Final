
import os
import csv
import time
import threading
import concurrent.futures as cf

def timing(fonction):
    def wrapper(*args, **kwargs):
        lock = threading.Lock()
        start = time.perf_counter()
        result = fonction(*args, **kwargs)
        exec_time = time.perf_counter() - start
        with lock:
            return result, exec_time
    return wrapper


def read_weather_data(filename):
    try: 
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for line in reader:
                yield {
                    "date": line["Date"],
                    "station": line["Station"],
                    "temperature": float(line["Temperature"]),
                    "pressure": float(line["Pressure"]),
                }
    except IOError as e:
        print(f"Error while reading {filename}: {e}")


@timing
def read_analyze(file):
    data = read_weather_data(file)
    stations = []
    temp = []
    pressure = []
    nb_lecture = 0
    for line in data:
        nb_lecture += 1
        temp.append(line["temperature"])
        pressure.append(line["pressure"])
        if line["station"] not in stations:
            stations.append(line["station"])
    return {
        "avg_temp": sum(temp) / len(temp),
        "max_temp": max(temp),
        "min_temp": min(temp),
        "avg_pressure": sum(pressure) / len(pressure),
        "nb_lectures": nb_lecture,
        "nb_unique_stations": len(stations),
    }


def process_files_concurrently(filenames):
    executor = cf.ThreadPoolExecutor(max_workers=10)
    results = {}
    with cf.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(read_analyze, file): file for file in filenames}
        for future in cf.as_completed(futures):
            file = futures[future]
            stats, exec_time = future.result()
            results[file] = {"stats": stats, "exec_time": exec_time}
    return results


def write_report(filenames):
    data = process_files_concurrently(filenames)
    print(" === Weather Analysis Report === \n")
    print("--- Statistics by File ---")
    for filename, filedata in data.items():
        print(f"File: {filename}")
        print(f"Processed in {filedata['exec_time']} seconds")
        print(f"    Records: {filedata['stats']['nb_lectures']}")
        print(f"    Avg Temperature: {filedata['stats']['avg_temp']:.2f}°C")
        print(f"    Min Temperature: {filedata['stats']['min_temp']:.2f}°C")
        print(f"    Max Temperature: {filedata['stats']['max_temp']:.2f}°C")
        print(f"    Avg Pressure: {filedata['stats']['avg_pressure']:.2f} hPa")
        print(f"    Unique Stations: {filedata['stats']['nb_unique_stations']}")
        print()


def main() -> None:
    print("Hello from weather-analyzer!")
    folder = "../data/"
    files = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(".csv")]
    write_report(files)
