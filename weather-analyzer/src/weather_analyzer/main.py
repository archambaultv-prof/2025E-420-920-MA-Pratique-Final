import csv
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Generator


def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        return (result, end_time - start_time)

    return wrapper


def process_files_concurrently(paths: list) -> dict:
    futures = []
    stats = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        for file in paths:
            future = executor.submit(process_file, read_weather_data(file), file)
            futures.append(future)
        for f in futures:
            (key, stat), time = f.result()
            stat["timing"] = time
            stats[key] = stat
    return stats


@timing
def process_file(iter: Generator, path: str):
    stats = {
        "avg_temp": 0,
        "min_temp": 0,
        "max_temp": 0,
        "avg_pressure": 0,
        "nb_row": 0,
        "unq_station": 0,
        "timing": 0,
    }

    station_set = set()
    for row in iter:
        stats["nb_row"] += 1
        for k, v in row.items():
            if k == "Date":
                continue
            if k == "Station" and v not in station_set:
                station_set.add(v)
            if k == "Temperature":
                stats["avg_temp"] += v
                if v > stats["max_temp"]:
                    stats["max_temp"] = v
                if v < stats["min_temp"]:
                    stats["min_temp"] = v
            if k == "Pressure":
                stats["avg_pressure"] += v
    stats["avg_temp"] = round(stats["avg_temp"] / stats["nb_row"])
    stats["avg_pressure"] = round(stats["avg_pressure"] / stats["nb_row"])
    stats["unq_station"] = len(station_set)
    return (path, stats)


def read_weather_data(path):
    with open(path, "r", encoding="UTF-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["Temperature"] = float(row["Temperature"])
            row["Pressure"] = float(row["Pressure"])
            yield row


def print_report(stats: dict):
    print("=== Weather Analysis Report ===")
    print("--- Statistics by File ---")
    for name, stat_dict in stats.items():
        print(f"File: {name}")
        print(f"Processed in {stat_dict['timing']:.6f} seconds")
        print(f"Records: {stat_dict['nb_row']}")
        print(f"Avg Temperature: {stat_dict['avg_temp']}°C")
        print(f"Min Temperature: {stat_dict['min_temp']}°C")
        print(f"Max Temperature: {stat_dict['max_temp']}°C")
        print(f"Avg Pressure: {stat_dict['avg_pressure']} hPa")
        print(f"Unique Stations: {stat_dict['unq_station']}")
        print("")


def main() -> None:
    files = ["../data/report1.csv", "../data/report2.csv", "../data/report3.csv"]
    stat_dict = process_files_concurrently(files)
    print_report(stat_dict)
