from concurrent.futures import ThreadPoolExecutor, as_completed
import csv 
import time
import os 

def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        temps_ecoule = end_time - start_time
        
        return result, temps_ecoule
    return wrapper

class Dataset():
    def __init__(self):
        pass
    @timing
    def  stats(self, file_path: str):
        reader = read_weather_data(file_path)
        count = 0
        sum_temp = 0.0
        sum_pressure = 0.0
        min_temp = float('inf')
        max_temp = float('-inf')
        stations = set()
        for row in reader:
            temp = row["Temperature"]
            press = row["Pressure"]
            station = row["Station"]
            count += 1
            sum_temp += temp
            sum_pressure += press
            min_temp = min(min_temp, temp)
            max_temp = max(max_temp, temp)
            stations.add(station)
        if count == 0:
            records = 0
            avg_temp = 0.0
            avg_pressure = 0.0
            min_temp = None
            max_temp = None
            unique_stations = 0
        else:
            avg_temp = sum_temp / count
            avg_pressure = sum_pressure / count
            unique_stations = len(stations)
            records = count
        return {
            "records": records,
            "avg_temp": avg_temp,
            "min_temp": min_temp,
            "max_temp": max_temp,
            "avg_pressure": avg_pressure,
            "unique_stations": unique_stations
        }
    def afficher_stats(self, stats: dict,file_path: str, exec_time: float):
        print(f"File: {file_path}")
        print(f"Processing time: {exec_time:.4f} seconds")
        for key, value in stats.items():
            if value is None:
                print(f"{key}: No data available")
                continue
            if key == "records":
                print(f"Number of records: {value}")
            elif key == "avg_temp":
                print(f"Average temperature: {value:.2f} °C")
            elif key == "min_temp":
                print(f"Minimum temperature: {value:.2f} °C")
            elif key == "max_temp":
                print(f"Maximum temperature: {value:.2f} °C")
            elif key == "avg_pressure":
                print(f"Average pressure: {value:.2f} hPa")
            elif key == "unique_stations":
                print(f"Number of unique stations: {value}")
                print("\n")


        
""" generator of weather data from a file """    
def read_weather_data(file_path: str) :
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                value = {}
                # Fusionner les colonnes si des virgules se trouvent dans les valeurs numériques
                if len(row) != 4:
                    continue
                date = row[0]
                station = row[1]
                temperature = float(row[2])
                pressure = float(row[3])
                value = { "Date": date, "Station": station, "Temperature": temperature, "Pressure": pressure}
                yield value

def process_files_concurrently(file_paths):
    workers = max(1, min(10, len(file_paths)))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        data = Dataset()
        futures = []
        future_to_path = {}
        results = {}
        for path in file_paths:
            future = executor.submit(data.stats, path)
            futures.append(future)
            future_to_path[future] = path
        for future in as_completed(futures):
            path = future_to_path[future]
            stats_dict, exec_time = future.result()
            results[path] = {"stats": stats_dict, "exec_time": exec_time}

        return results


base_dir = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(base_dir,".." ,"..", "data"))



def main():
    files = [
        os.path.join(data_dir, "report1.csv"),
        os.path.join(data_dir, "report2.csv"),
        os.path.join(data_dir, "report3.csv"),
        os.path.join(data_dir, "report4.csv"),
        os.path.join(data_dir, "report5.csv"),
        os.path.join(data_dir, "report6.csv"),
        os.path.join(data_dir, "report7.csv"),
        os.path.join(data_dir, "report8.csv"),
        os.path.join(data_dir, "report9.csv"),

    ]
    data = Dataset()
    results = process_files_concurrently(files)
    print("=== Weather Analysis Report ===\n")
    print("--- Statistics by File ---")
    for file_path, result in results.items():
        data.afficher_stats(result["stats"], file_path, result["exec_time"])


if __name__ == "__main__":
    main()
