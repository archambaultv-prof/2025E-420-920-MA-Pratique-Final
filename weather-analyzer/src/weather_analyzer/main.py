from pathlib import Path;
import csv
import time
import concurrent.futures
import random
import os

def main() -> None:
    print("Hello from weather-analyzer!")
    weather_files = list(get_files_by_extension("../../../data", ".csv"))
    reports=process_files_concurrently(weather_files)

    for v in reports.values():
        print(v[0])

    

def read_csv(file):
    with open(file, 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {
                "Date":row["Date"],
                "Station:":row["Station"],
                "Temperature":float(row["Temperature"]),
                "Pressure":float(row["Pressure"])
                }
            


def timing(func):
    def wrapper(*args, **kwargs):
        debut = time.time()
        time.sleep(random.uniform(0.01,0.05))
        resultat = func(*args, **kwargs)
        fin = time.time()
        print(f"{fin-debut:.2f}")
        return (resultat,fin-debut)
    return wrapper


@timing
def calculate_stats(file):
    data =list(read_csv(file))

    filename=os.path.basename(file)

    avg_temp = sum([line['Temperature'] for line in data])/len(data)
    min_temp= min([line['Temperature'] for line in data])
    max_temp= max([line['Temperature'] for line in data])
    avg_pres=sum([line['Pressure'] for line in data])/len(data)
    lectures = len(data)
    unique_stations = len(set([line['Station:'] for line in data]))
    
    return f"""
    === Weather Analysis Report ===

    --- Statistics by File ---
    File: {filename}\n
    Processed in 0.03 seconds
    Records: {lectures}\n
    Avg Temperature: {avg_temp:.2f}°C
    Min Temperature: {min_temp:.2f}°C
    Max Temperature: {max_temp:.2f}°C
    Avg Pressure: {avg_pres:.2f} hPa
    Unique Stations: {unique_stations}
   """

def process_files_concurrently(files:list):

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures=executor.map(calculate_stats,files)

    filenames = [os.path.basename(path) for path in files]
    stats_per_file ={}

    for file,res in zip(filenames,futures):
        stats_per_file[file]=res
    
    return stats_per_file

def get_files_by_extension(directory_path, extension):
    
    path = Path(directory_path)
    if not path.is_dir():
        raise FileNotFoundError(f"The directory '{directory_path}' does not exist.")

    # Use rglob to recursively find files matching the pattern
    # The pattern includes the extension, e.g., "*.txt"
    found_files = list(path.rglob(f"*{extension}"))
    return found_files


class WeatherData:
    def __init__(self,date,station,temp,pressure) -> None:
        self.date=date
        self.station=station
        self.temp=temp
        self.pressure=pressure


