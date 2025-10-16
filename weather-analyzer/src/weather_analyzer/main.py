from pathlib import Path;
import csv
import time
import concurrent.futures


def main() -> None:
    print("Hello from weather-analyzer!")

def read_csv(file):
    with open(file, 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d_row = {
                "Date":row["Date"],
                "Station:":row["Station"],
                "Temperature":float(row["Temperature"]),
                "Pressure":float(row["Pressure"])
                }
            yield d_row


def mesurer_temps(func):
    def wrapper(*args, **kwargs):
        debut = time.time()
        resultat = func(*args, **kwargs)
        fin = time.time()
        return (resultat,fin-debut)
    return wrapper

def calculate_stats(file):
    pass


def process_files_conurrently(files:list):

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures=executor.map(calculate_stats,files)
    
    stats_per_file ={}

    for file,res in zip(files,futures):
        stats_per_file[file]=res
    
    return stats_per_file